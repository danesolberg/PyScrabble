from collections import namedtuple
from copy import copy
import gaddag
from gaddag.gaddag import GADDAG
from gaddag.cgaddag import cgaddag
import sys
import logging
from .word import Word
from .exceptions import AnchorSquareError, StartingSquareError


#  PyGADDAG monkey patch for python < 3.7
if sys.version_info < (3, 7):
    def add_word(self, word):
        """
        Add a word to the GADDAG.

        Args:
            word: A word to be added to the GADDAG.
        """
        word = word.lower()

        if not word.isalpha():
            raise ValueError("Invalid character in word '{}'".format(word))

        word = word.encode(encoding="ascii")
        result = cgaddag.gdg_add_word(self.gdg, word)
        if result == 1:
            raise ValueError("Invalid character in word '{}'".format(word))
        elif result == 2:
            raise MemoryError("Out of memory, GADDAG is in an undefined state")

    GADDAG.add_word = add_word

logging.basicConfig(filename="playHistory.log", level=logging.INFO)


class MoveGenerator:
    Move = namedtuple('Move', ['word','square','direction','score'])
    Arc = namedtuple('Arc', ['left','right','up','down'])

    def __init__(self, game, dic_path):
        self.game = game
        self.board = game.get_board()
        self.gdg = gaddag.GADDAG()
        self.dic_path = dic_path
        self.moves = []
        self.cross_sets = [['' for x in range(self.board.BOARD_WIDTH)] for y in range(self.board.BOARD_HEIGHT)]
        self.load_gaddag()
        self.set_cross_sets()
        self.last_turn_generated = game.get_turn()

    def load_gaddag(self):
        with open(self.dic_path,'r') as dic:
            for line in dic:
                self.gdg.add_word(line.strip('\n'))

    def prefix_path(self, square, is_first=True):
        if is_first and not self.board.get_below_square(square).get_tile():
            raise ValueError('Cannot build prefix for this square.')
        if self.board.get_below_square(square).get_tile():
            if is_first:
                letter = ''
            else:
                letter = square.get_tile().get_letter()
            path = self.prefix_path(self.board.get_below_square(square), is_first=False) + letter
        else:
            letter = square.get_tile().get_letter()
            return letter
        return path.lower()

    def suffix_path(self, square, is_first=True):
        if is_first and not self.board.get_above_square(square).get_tile():
            raise ValueError('Cannot build suffix for this square.')
        if self.board.get_above_square(square).get_tile():
            if is_first:
                letter = ''
            else:
                letter = square.get_tile().get_letter()
            path = letter + self.suffix_path(self.board.get_above_square(square), is_first=False)
        else:
            letter = square.get_tile().get_letter()
            return letter
        if is_first:
            path = path + '+'
        return path.lower()

    def is_anchor_square(self, square):
        adjacent_square = self.board.get_adjacent_square(square)
        if square.is_empty() and (not adjacent_square.up.is_empty() or not adjacent_square.down.is_empty() or not adjacent_square.left.is_empty() or not adjacent_square.right.is_empty()):
            return True
        elif square.get_coord() == (7,7) and square.is_empty():
            return True
        else:
            return False

    def find_anchor(self, placement_square, direction):
        current_square = placement_square
        if self.is_anchor_square(current_square):
            return current_square
        if direction == 'r':
            while not self.is_anchor_square(current_square) and self.board.get_adjacent_square(current_square).right.is_in_bounds():
                right_square = self.board.get_adjacent_square(current_square).right
                current_square = right_square
                if self.is_anchor_square(current_square):
                    return current_square
        if direction == 'd':
            while not self.is_anchor_square(current_square) and self.board.get_adjacent_square(current_square).down.is_in_bounds():
                down_square = self.board.get_adjacent_square(current_square).down
                current_square = down_square
                if self.is_anchor_square(current_square):
                    return current_square
        if self.game.turn > 1:
            raise AnchorSquareError()
        else:
            raise StartingSquareError()

    def get_adjacent_arc(self, square, direction=None, is_first=True):
        left_arc=right_arc=up_arc=down_arc = ''
        #  up arc (anchor square above tile)
        if (is_first and not self.board.get_adjacent_square(square).down.is_empty()) or direction=='up':
            if self.board.get_adjacent_square(square).down.is_empty():
                return square.get_tile().get_letter()
            else:
                up_arc = self.get_adjacent_arc(self.board.get_adjacent_square(square).down, 'up', False)
                if is_first:
                    up_arc = up_arc#.lower()
                else:
                    return up_arc + square.get_tile().get_letter()

        #  down arc (anchor square below tile)
        if (is_first and not self.board.get_adjacent_square(square).up.is_empty()) or direction=='down':
            if self.board.get_adjacent_square(square).up.is_empty():
                return square.get_tile().get_letter()
            else:
                down_arc = self.get_adjacent_arc(self.board.get_adjacent_square(square).up, 'down', False)
                if is_first:
                    down_arc = down_arc + '+'
                else:
                    return square.get_tile().get_letter() + down_arc

        #  left arc (anchor square left of tile)
        if (is_first and not self.board.get_adjacent_square(square).right.is_empty()) or direction=='left':
            if self.board.get_adjacent_square(square).right.is_empty():
                return square.get_tile().get_letter()
            else:
                left_arc = self.get_adjacent_arc(self.board.get_adjacent_square(square).right, 'left', False)
                if is_first:
                    left_arc = left_arc#.lower()
                else:
                    return left_arc + square.get_tile().get_letter()

        #  right arc (anchor square right of tile)
        if (is_first and not self.board.get_adjacent_square(square).left.is_empty()) or direction=='right':
            if self.board.get_adjacent_square(square).left.is_empty():
                return square.get_tile().get_letter()
            else:
                right_arc = self.get_adjacent_arc(self.board.get_adjacent_square(square).left, 'right', False)
                if is_first:
                    right_arc = right_arc + '+'
                else:
                    return square.get_tile().get_letter() + right_arc

        return self.Arc(left_arc,right_arc,up_arc,down_arc)

    def letter_set_exterior(self, path):
        node = self.gdg.root
        try:
            node = node.follow(path)
        except:
            return ''
        letter_set = ''.join(map(str, node.letter_set))
        return letter_set.upper()

    def letter_set_interior(self, square):
        def check_letter(square, arc, letter):
            try:
                new_arc = arc[letter]
            except:
                if arc.is_end(letter) is False or not self.board.get_adjacent_square(square).down.is_empty():
                    return False
            if self.board.get_adjacent_square(square).down.is_empty():
                if arc.is_end(letter):
                    return True
                else:
                    return False
            else:
                new_square = self.board.get_adjacent_square(square).down
                new_letter = new_square.get_tile().get_letter()
                res = check_letter(new_square, new_arc, new_letter)
                return res

        cross_set_interior = []
        suf_path = self.get_adjacent_arc(square).down
        try:
            suf_edge = self.gdg.root.follow(suf_path).edges
        except:
            return ''
        for cross in suf_edge:
            arc = self.gdg.root.follow(suf_path)
            if check_letter(square, arc, cross) is True:
                cross_set_interior.append(cross)

        cross_set_interior = ''.join(map(str, cross_set_interior))
        return cross_set_interior.upper()

    def get_anchor_squares(self):
        anchor_squares = []
        if self.game.get_turn() == 1:
            anchor_squares.append(self.board.get_square((7,7)))
        for row in self.board.get_board_arr():
            for square in row:
                if square.get_tile() or square in anchor_squares:
                    continue
                elif self.is_anchor_square(square):
                    anchor_squares.append(square)
        return anchor_squares

    #  always horizontal. transpose board and run again before vertical moves
    def cross_set(self, square):
        cross_set = ''

        if square.get_tile():
            raise ValueError('Only empty squares can have cross sets.')
        elif self.board.get_adjacent_square(square).up.is_empty() and self.board.get_adjacent_square(square).down.is_empty():
            cross_set = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        elif not self.board.get_adjacent_square(square).up.is_empty() and not self.board.get_adjacent_square(square).down.is_empty():
            cross_set = self.letter_set_interior(square)
        elif not self.board.get_adjacent_square(square).up.is_empty(): #  suffix
            letter_set = self.letter_set_exterior(self.get_adjacent_arc(square).down)
            cross_set = letter_set
        elif not self.board.get_adjacent_square(square).down.is_empty(): #  prefix
            letter_set = self.letter_set_exterior(self.get_adjacent_arc(square).up)
            cross_set = letter_set
        return cross_set

    def set_cross_sets(self):
        for row in self.board.get_board_arr():
            for square in row:
                coord = square.get_coord()
                if square.is_empty():
                    self.cross_sets[coord.y][coord.x] = self.cross_set(square)
                else:
                    self.cross_sets[coord.y][coord.x] = ''

    def record_move(self, word, square, direction):
        if direction == 'd':
            coord = square.get_coord()
            square_debug = square
            square = self.board.get_square((coord.y,coord.x))
        try:
            score = Word(self.game, word, square.get_coord(), 'r').get_score()
            move = self.Move(word, square, direction, score)
            self.moves.append(move)
        except Exception as e:
            raise e

    def clear_moves(self):
        #  TODO save current moves to log json, then clear
        self.moves = []
        return self.moves

    def get_moves(self):
        return set(self.moves)

    #  gen() and go_on() functions lifted from Appel and Jacobson "The World's Fastest Scrabble Program" (1988)
    #  https://www.cs.cmu.edu/afs/cs/academic/class/15451-s06/www/lectures/scrabble.pdf
    def gen(self, anchor, rack_arr, direction, arc = None, pos = 0, word = '', place_pos = 0):
        if arc is None:
            arc = self.gdg.root
        anchor_coord = anchor.get_coord()
        square = self.board.get_square((anchor_coord.y, anchor_coord.x + pos))
        rack = copy(rack_arr)
        place_pos = min(pos, place_pos)
        if square.get_tile():
            letter = square.get_tile().get_letter()
            if letter.lower() in arc.edges:
                new_arc = arc[letter]
                self.go_on(anchor, pos, letter, word, rack, new_arc, arc, place_pos, direction)
        elif len(rack) > 0:
            for tile in rack:
                letter = tile.get_letter()
                cross_set = self.cross_sets[anchor_coord.y][anchor_coord.x + pos]
                if letter in cross_set:
                    if letter.lower() in arc.edges:
                        new_arc = arc[letter]
                        new_rack = copy(rack)
                        new_rack.remove(tile)
                        self.go_on(anchor, pos, letter, word, new_rack, new_arc, arc, place_pos, direction)
            if any(tile.get_is_blank() for tile in rack):
                tile = [tile for tile in rack if tile.get_is_blank() == True][0]
                for letter in cross_set:
                    if letter.lower() in arc.edges:
                        new_arc = arc[letter]
                        new_rack = copy(rack)
                        new_rack.remove(tile)
                        self.go_on(anchor, pos, letter, word, new_rack, new_arc, arc, place_pos, direction)

    def go_on(self, anchor, pos, letter, word, rack, new_arc, old_arc, place_pos, direction):
        anchor_coord = anchor.get_coord()
        square = self.board.get_square((anchor_coord.y, anchor_coord.x + pos))
        if pos <= 0: #  moving left, creating prefix
            word = letter + word
            if old_arc.is_end(letter) and self.board.get_adjacent_square(square).left.is_empty() and self.board.get_adjacent_square(anchor).right.is_empty():
                placement_square = self.board.get_square((anchor_coord.y, anchor_coord.x + place_pos))
                try:
                    self.record_move(word, placement_square, direction)
                except Exception as e:
                    raise e
            if new_arc.edges:
                if self.board.get_adjacent_square(square).left.is_in_bounds():
                    self.gen(anchor, rack, direction, new_arc, pos - 1, word, place_pos)
                    if '+' in new_arc.edges:
                        new_arc = new_arc['+'] #  change direction
                        if new_arc.edges and self.board.get_adjacent_square(square).left.is_empty() and self.board.get_adjacent_square(anchor).right.is_in_bounds():
                            self.gen(anchor, rack, direction, new_arc, 1, word, place_pos)
        elif pos > 0: #  moving right, creating suffix
            word = word + letter
            if old_arc.is_end(letter) and self.board.get_adjacent_square(square).right.is_empty() and self.board.get_adjacent_square(square).right.is_in_bounds():
                placement_square = self.board.get_square((anchor_coord.y, anchor_coord.x + place_pos))
                try:
                    self.record_move(word, placement_square, direction)
                except Exception as e:
                    raise e
            if new_arc.edges and self.board.get_adjacent_square(square).right.is_in_bounds():
                self.gen(anchor, rack, direction, new_arc, pos + 1, word, place_pos)

    def generate_moves(self, rack_arr, specific_square = None):
        if self.game.get_turn() == self.last_turn_generated:
            return self.get_moves()
        
        self.clear_moves()
        anchors = self.get_anchor_squares()

        for i in range(2):
            self.set_cross_sets()
            if i == 0:
                direction = 'r' #  right / horizontal
            else:
                direction = 'd' #  down / vertical

            if specific_square is None:
                for square in anchors:
                    self.gen(square, rack_arr, direction)
            else:
                self.gen(specific_square, rack_arr, direction)
            self.board.transpose_board()
        
        self.last_turn_generated = self.game.get_turn()
        return self.get_moves()