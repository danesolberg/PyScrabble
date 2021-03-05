from collections import defaultdict
from copy import copy

from pyscrabble.game_engine.tile import Tile


class Word:
    def __init__(self, game, word, location, direction):
        self.game = game
        self.board = game.get_board()
        self.word = word
        self.location = location
        self.direction = direction
        self.current_player = game.get_current_player()
        self.squares = self.set_squares()
        self.required_letters = self.set_required_letters()
        self.word_placement = self.set_word_placement()
        self.secondary_word_placements = self.get_secondary_word_placements()
        self.score = self.calculate_score()

    def get_word_str(self):
        return self.word

    def get_location(self):
        return self.location

    def get_direction(self):
        return self.direction

    def get_length(self):
        return len(self.word)

    def get_score(self):
        return self.score

    def set_squares(self):
        coord = self.location

        squares = []
        square = self.board.get_square(coord)
        squares.append(square)

        for _ in range(self.get_length() - 1):
            if self.direction == 'r':
                coord = (coord[0], coord[1] + 1)
                square = self.board.get_square(coord)
                squares.append(square)
            elif self.direction == 'd':
                coord = (coord[0] + 1, coord[1])
                square = self.board.get_square(coord)
                squares.append(square)
            else:
                raise ValueError('Incorrect direction entered.')
        return squares

    def get_squares(self):
        return self.squares

    def set_word_placement(self):
        """
            Sets self.word_placement using the following pattern
            [(Square,Tile),(Square,Tile)]
        """
        word_placement = []
        rack_letter_map = defaultdict(list)
        for tile in self.current_player.rack.get_rack_arr():
            rack_letter_map[tile.get_letter()].append(tile)

        for i, square in enumerate(self.squares):
            if square.get_tile():
                word_placement.append((square, square.get_tile()))
            else:
                current_required_letter = self.word[i]
                if current_required_letter not in rack_letter_map:
                    if Tile.BLANK_SYMBOL in rack_letter_map:
                        tile = copy(rack_letter_map[Tile.BLANK_SYMBOL].pop())
                        tile.set_blank_letter(self.word[i])
                        word_placement.append((square, tile))
                        if not rack_letter_map[Tile.BLANK_SYMBOL]:
                            del rack_letter_map[Tile.BLANK_SYMBOL]
                else:
                    tile = rack_letter_map[current_required_letter].pop()
                    if not rack_letter_map[current_required_letter]:
                        del rack_letter_map[current_required_letter]
                    word_placement.append((square, tile))
        return word_placement

    def set_required_letters(self):
        required_letters = []
        for i, square in enumerate(self.squares):
            if not square.get_tile():
                required_letters.append(self.word[i].upper())
        return required_letters

    def get_word_placement(self):
        return self.word_placement

    def get_required_letters(self):
        return self.required_letters

    def get_secondary_word_placements(self):
        def word_placement(board, starting_square, primary_cross_square, primary_cross_tile, direction):
            square = starting_square
            word_arr = []
            while not square.is_empty() or square is primary_cross_square:
                if not square.is_empty():
                    tile = square.get_tile()
                else:
                    tile = primary_cross_tile

                word_arr.append((square, tile))

                if direction == 'r':
                    square = board.get_adjacent_square(square, "below")
                elif direction == 'd':
                    square = board.get_adjacent_square(square, "right")

            return word_arr

        all_secondary_word_placements = []

        for square, tile in self.word_placement:
            if self.direction == 'r':
                #  check up and down tiles
                #  get position of most vertical conjoining square for each square in placed word
                starting_square = square
                while not self.board.get_adjacent_square(starting_square, "above").is_empty():
                    starting_square = self.board.get_adjacent_square(starting_square, "above")
                secondary_word_placement = word_placement(self.board, starting_square, square, tile, self.direction)
                all_secondary_word_placements.append(secondary_word_placement)
            elif self.direction =='d':
                #  check left and right tiles
                #  get position of left-most conjoining square for each square in placed word
                starting_square = square
                while not self.board.get_adjacent_square(starting_square, "left").is_empty():
                    starting_square = self.board.get_adjacent_square(starting_square, "left")
                secondary_word_placement = word_placement(self.board, starting_square, square, tile, self.direction)
                all_secondary_word_placements.append(secondary_word_placement)
        #  secondary words must be at least 2 tiles long
        all_secondary_word_placements = [word for word in all_secondary_word_placements
                                         if len(word) > 1
                                         and any(tile for square, tile in word if square.is_empty())]

        return all_secondary_word_placements

    def get_secondary_words(self):
        word_arr = [''.join([tile.get_letter() for square, tile in placement]) for placement in self.secondary_word_placements]
        return word_arr

    def calculate_score(self):
        def score_word(word_placement):
            word_multipliers = []
            word_score = 0
            for square, tile in word_placement:
                tile_score = tile.get_score()

                if square.is_empty():
                    multiplier = square.get_multiplier()

                    if multiplier in ['TWS', 'DWS']:
                        word_multipliers.append(multiplier)
                    elif multiplier == 'TLS':
                        tile_score *= 3
                    elif multiplier == 'DLS':
                        tile_score *= 2
                word_score += tile_score
            for multiplier in word_multipliers:
                if multiplier == 'TWS':
                    word_score *= 3
                elif multiplier == 'DWS':
                    word_score *= 2
            return word_score

        def calculate_primary(self):
            primary_score = score_word(self.word_placement)
            if len(self.required_letters) == 7:
                primary_score += 50
            return primary_score

        def calculate_secondary(self):
            secondary_score = 0
            for word_placement in self.secondary_word_placements:
                word_score = score_word(word_placement)
                secondary_score += word_score
            return secondary_score

        ps = calculate_primary(self)
        ss = calculate_secondary(self)
        return ps + ss
