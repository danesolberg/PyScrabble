from collections import namedtuple
from copy import copy
from gaddag.gaddag import Node
from gaddag.cgaddag import cgaddag

from . import gdg
from .word import Word
from .exceptions import AnchorSquareError, StartingSquareError


Move = namedtuple('Move', ['word', 'square', 'direction', 'score'])
Arc = namedtuple('Arc', ['above', 'below', 'left', 'right'])


class MoveGenerator:
    EMPTY_NODE = Node(cgaddag.gdg_create().contents, 0)

    def __init__(self, game):
        self.game = game
        self.board = game.get_board()
        self.moves = []
        self.cross_sets = [['' for x in range(self.board.BOARD_DIMENSIONS)] for y in range(self.board.BOARD_DIMENSIONS)]
        self.set_cross_sets()
        self.last_turn_generated = game.get_turn()

    def prefix_path(self, square, is_first=True):
        if is_first and not self.board.get_adjacent_square(square, "below").get_tile():
            raise ValueError('Cannot build prefix for this square.')
        if self.board.get_adjacent_square(square, "below").get_tile():
            if is_first:
                letter = ''
            else:
                letter = square.get_tile().get_letter()
            path = self.prefix_path(self.board.get_adjacent_square(square, "below"), is_first=False) + letter
        else:
            letter = square.get_tile().get_letter()
            return letter
        return path.lower()

    def suffix_path(self, square, is_first=True):
        if is_first and not self.board.get_adjacent_square(square, "above").get_tile():
            raise ValueError('Cannot build suffix for this square.')
        if self.board.get_adjacent_square(square, "above").get_tile():
            if is_first:
                letter = ''
            else:
                letter = square.get_tile().get_letter()
            path = letter + self.suffix_path(self.board.get_adjacent_square(square, "above"), is_first=False)
        else:
            letter = square.get_tile().get_letter()
            return letter
        if is_first:
            path = path + '+'
        return path.lower()

    def is_anchor_square(self, square):
        adjacent_squares = self.board.get_adjacent_squares(square)
        if square.is_empty() and (not adjacent_squares.above.is_empty() or not adjacent_squares.below.is_empty() or \
                                  not adjacent_squares.left.is_empty() or not adjacent_squares.right.is_empty()):
            return True
        elif square.get_coord() == (7, 7) and square.is_empty():
            return True
        else:
            return False

    def find_anchor(self, placement_square, direction):
        current_square = placement_square
        if self.is_anchor_square(current_square):
            return current_square
        if direction == 'r':
            while not self.is_anchor_square(current_square) and self.board.get_adjacent_square(current_square, "right").is_in_bounds():
                right_square = self.board.get_adjacent_square(current_square, "right")
                current_square = right_square
                if self.is_anchor_square(current_square):
                    return current_square
        if direction == 'd':
            while not self.is_anchor_square(current_square) and self.board.get_adjacent_square(current_square, "below").is_in_bounds():
                down_square = self.board.get_adjacent_square(current_square, "below")
                current_square = down_square
                if self.is_anchor_square(current_square):
                    return current_square
        if self.game.turn > 1:
            raise AnchorSquareError()
        else:
            raise StartingSquareError()

    def get_adjacent_arc(self, square, direction=None, is_first=True):
        left_arc = right_arc = up_arc = down_arc = ''

        # up arc (anchor square above tile)
        if (is_first and not self.board.get_adjacent_square(square, "below").is_empty()) or direction == 'above':
            if self.board.get_adjacent_square(square, "below").is_empty():
                return square.get_tile().get_letter()
            else:
                up_arc = self.get_adjacent_arc(self.board.get_adjacent_square(square, "below"), 'above', False)
                if is_first:
                    up_arc = up_arc
                else:
                    return up_arc + square.get_tile().get_letter()

        # down arc (anchor square below tile)
        if (is_first and not self.board.get_adjacent_square(square, "above").is_empty()) or direction == 'below':
            if self.board.get_adjacent_square(square, "above").is_empty():
                return square.get_tile().get_letter()
            else:
                down_arc = self.get_adjacent_arc(self.board.get_adjacent_square(square, "above"), 'below', False)
                if is_first:
                    down_arc = down_arc + '+'
                else:
                    return square.get_tile().get_letter() + down_arc

        # left arc (anchor square left of tile)
        if (is_first and not self.board.get_adjacent_square(square, "right").is_empty()) or direction == 'left':
            if self.board.get_adjacent_square(square, "right").is_empty():
                return square.get_tile().get_letter()
            else:
                left_arc = self.get_adjacent_arc(self.board.get_adjacent_square(square, "right"), 'left', False)
                if is_first:
                    left_arc = left_arc
                else:
                    return left_arc + square.get_tile().get_letter()

        # right arc (anchor square right of tile)
        if (is_first and not self.board.get_adjacent_square(square, "left").is_empty()) or direction == 'right':
            if self.board.get_adjacent_square(square, "left").is_empty():
                return square.get_tile().get_letter()
            else:
                right_arc = self.get_adjacent_arc(self.board.get_adjacent_square(square, "left"), 'right', False)
                if is_first:
                    right_arc = right_arc + '+'
                else:
                    return square.get_tile().get_letter() + right_arc

        return Arc(up_arc, down_arc, left_arc, right_arc,)

    def letter_set_exterior(self, path):
        node = gdg.root
        try:
            node = node.follow(path)
        except Exception:
            return ''
        letter_set = set(map(str.upper, node.letter_set))
        return letter_set

    def letter_set_interior(self, square):
        def check_letter(square, arc, letter):
            try:
                new_arc = arc[letter]
            except Exception:
                if arc.is_end(letter) is False or not self.board.get_adjacent_square(square, "below").is_empty():
                    return False
            if self.board.get_adjacent_square(square, "below").is_empty():
                if arc.is_end(letter):
                    return True
                else:
                    return False
            else:
                new_square = self.board.get_adjacent_square(square, "below")
                new_letter = new_square.get_tile().get_letter()
                res = check_letter(new_square, new_arc, new_letter)
                return res

        cross_set_interior = []
        suf_path = self.get_adjacent_arc(square).below
        try:
            suf_edge = gdg.root.follow(suf_path).edges
        except Exception:
            return ''
        for cross in suf_edge:
            arc = gdg.root.follow(suf_path)
            if check_letter(square, arc, cross) is True:
                cross_set_interior.append(cross)

        cross_set_interior = set(map(str.upper, cross_set_interior))
        return cross_set_interior

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

    # always horizontal. transpose board and run again before vertical moves
    def cross_set(self, square):
        cross_set = ''
        adjacent_squares = self.board.get_adjacent_squares(square)

        if square.get_tile():
            raise ValueError('Only empty squares can have cross sets.')
        elif adjacent_squares.above.is_empty() and adjacent_squares.below.is_empty():
            cross_set = set(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        elif not adjacent_squares.above.is_empty() and not adjacent_squares.below.is_empty():
            cross_set = self.letter_set_interior(square)
        elif not adjacent_squares.above.is_empty():  # suffix
            letter_set = self.letter_set_exterior(self.get_adjacent_arc(square).below)
            cross_set = letter_set
        elif not adjacent_squares.below.is_empty():  # prefix
            letter_set = self.letter_set_exterior(self.get_adjacent_arc(square).above)
            cross_set = letter_set
        return cross_set

    def set_cross_sets(self):
        for row in self.board.get_board_arr():
            for square in row:
                coord = square.get_coord()
                if square.is_empty():
                    self.cross_sets[coord.y][coord.x] = self.cross_set(square)
                else:
                    self.cross_sets[coord.y][coord.x] = set()

    def record_move(self, word, square, direction):
        if direction == 'd':
            coord = square.get_coord()
            square = self.board.get_square((coord.y, coord.x))
        try:
            score = Word(self.game, word, square.get_coord(), 'r').get_score()
            move = Move(word, square, direction, score)
            self.moves.append(move)
        except Exception as e:
            raise e

    def clear_moves(self):
        self.moves = []
        return self.moves

    def get_moves(self):
        return set(self.moves)

    # gen() and go_on() functions lifted from Steven A. Gordon's "A Faster Scrabble Move Generation Algorithm" (1994)
    # https://ericsink.com/downloads/faster-scrabble-gordon.pdf
    def gen(self, anchor, rack_arr, direction, arc=None, pos=0, word='', place_pos=0):
        if arc is None:
            arc = gdg.root
        anchor_coord = anchor.get_coord()
        square = self.board.get_square((anchor_coord.y, anchor_coord.x + pos))
        rack = copy(rack_arr)
        place_pos = min(pos, place_pos)
        arc_edges = set(arc.edges)
        if square.get_tile():
            letter = square.get_tile().get_letter()
            if letter.lower() in arc_edges:
                new_arc = arc[letter]
                self.go_on(anchor, pos, letter, word, rack, new_arc, arc, place_pos, direction)
        elif len(rack) > 0:
            cross_set = self.cross_sets[anchor_coord.y][anchor_coord.x + pos]
            arc_letter_set = set(arc.letter_set)
            for tile in rack:
                if tile.get_is_blank():
                    continue
                letter = tile.get_letter()
                if letter in cross_set:
                    if letter.lower() in arc_edges:
                        new_arc = arc[letter]
                        new_rack = copy(rack)
                        new_rack.remove(tile)
                        self.go_on(anchor, pos, letter, word, new_rack, new_arc, arc, place_pos, direction)
                    elif letter.lower() in arc_letter_set:
                        new_arc = self.EMPTY_NODE
                        new_rack = copy(rack)
                        new_rack.remove(tile)
                        self.go_on(anchor, pos, letter, word, new_rack, new_arc, arc, place_pos, direction)
            blank_tile = next((tile for tile in rack if tile.get_is_blank()), None)
            if blank_tile:
                for letter in cross_set:
                    if letter.lower() in arc_edges:
                        new_arc = arc[letter]
                        new_rack = copy(rack)
                        new_rack.remove(blank_tile)
                        self.go_on(anchor, pos, letter, word, new_rack, new_arc, arc, place_pos, direction)
                    elif letter.lower() in arc_letter_set:
                        new_arc = self.EMPTY_NODE
                        new_rack = copy(rack)
                        new_rack.remove(tile)
                        self.go_on(anchor, pos, letter, word, new_rack, new_arc, arc, place_pos, direction)

    def go_on(self, anchor, pos, letter, word, rack, new_arc, old_arc, place_pos, direction):
        anchor_coord = anchor.get_coord()
        square = self.board.get_square((anchor_coord.y, anchor_coord.x + pos))
        if pos <= 0:  # moving left, creating prefix
            word = letter + word
            if old_arc.is_end(letter) and self.board.get_adjacent_square(square, "left").is_empty() and self.board.get_adjacent_square(anchor, "right").is_empty():
                placement_square = self.board.get_square((anchor_coord.y, anchor_coord.x + place_pos))
                try:
                    self.record_move(word, placement_square, direction)
                except Exception as e:
                    raise e
            if new_arc.edges:
                if self.board.get_adjacent_square(square, "left").is_in_bounds():
                    self.gen(anchor, rack, direction, new_arc, pos - 1, word, place_pos)
                if '+' in new_arc.edges:
                    new_arc = new_arc['+']  # change direction
                    if (new_arc.edges or new_arc.letter_set) and self.board.get_adjacent_square(square, "left").is_empty() and self.board.get_adjacent_square(anchor, "right").is_in_bounds():
                        self.gen(anchor, rack, direction, new_arc, 1, word, place_pos)
        elif pos > 0:  # moving right, creating suffix
            word = word + letter
            if old_arc.is_end(letter) and self.board.get_adjacent_square(square, "right").is_empty(): # and self.board.get_adjacent_squares(square).right.is_in_bounds():
                placement_square = self.board.get_square((anchor_coord.y, anchor_coord.x + place_pos))
                try:
                    self.record_move(word, placement_square, direction)
                except Exception as e:
                    raise e
            if (new_arc.edges or new_arc.letter_set) and self.board.get_adjacent_square(square, "right").is_in_bounds():
                self.gen(anchor, rack, direction, new_arc, pos + 1, word, place_pos)

    def generate_moves(self, rack_arr, specific_square=None):
        if self.game.get_turn() == self.last_turn_generated:
            return self.get_moves()
        
        self.clear_moves()
        anchors = self.get_anchor_squares()

        for i in range(2):
            self.set_cross_sets()
            if i == 0:
                direction = 'r'  # right / horizontal
            else:
                direction = 'd'  # down / vertical

            if specific_square is None:
                for square in anchors:
                    self.gen(square, rack_arr, direction)
            else:
                self.gen(specific_square, rack_arr, direction)
            self.board.transpose_board()
        
        self.last_turn_generated = self.game.get_turn()
        return self.get_moves()
