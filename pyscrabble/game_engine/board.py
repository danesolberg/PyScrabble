from collections import namedtuple
from .square import Square
from .exceptions import CoordinateError

Adjacent_Squares = namedtuple('Adjacent_Square', ['above', 'below', 'left', 'right'])


class Board:
    BOARD_DIMENSIONS = 15
    STARTING_SQUARE = (7, 7)
    PREMIUM_SQUARES = {
        'TWS': [(0, 0), (7, 0), (14, 0), (0, 7), (14, 7), (0, 14), (7, 14), (14, 14)],
        'DWS': [(1, 1), (2, 2), (3, 3), (4, 4), (1, 13), (2, 12), (3, 11), (4, 10), (13, 1), (12, 2), (11, 3), (10, 4),
                (13, 13), (12, 12), (11, 11), (10, 10)],
        'TLS': [(1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13), (9, 1), (9, 5), (9, 9), (9, 13), (13, 5), (13, 9)],
        'DLS': [(0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (6, 6), (6, 8), (6, 12), (7, 3),
                (7, 11), (8, 2), (8, 6), (8, 8), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3),
                (14, 11)]
    }
    OFF_BOARD_SQUARE = Square((-1, -1))

    ADJACENT_DIRECTIONS = {
        "above": (-1, 0),
        "below": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }

    def __init__(self):
        self.board = [tuple(Square((y, x)) for x in range(Board.BOARD_DIMENSIONS)) for y in range(Board.BOARD_DIMENSIONS)]
        self.initialize_premium_squares()
        self.last_played_tiles = []

    def get_square(self, coord):
        try:
            return self.board[coord[0]][coord[1]]
        except IndexError:
            raise CoordinateError(coord)

    def initialize_premium_squares(self):
        self.get_square(Board.STARTING_SQUARE).set_text('*')
        self.get_square(Board.STARTING_SQUARE).set_multiplier('DWS')

        for multiplier in Board.PREMIUM_SQUARES:
            for coord in Board.PREMIUM_SQUARES[multiplier]:
                self.get_square(coord).set_text(multiplier)
                self.get_square(coord).set_multiplier(multiplier)

    def place_tiles_on_board(self, word):
        placement = word.get_word_placement()
        self.reset_last_play_cue()
        for pair in placement:
            square = pair[0]
            tile = pair[1]
            if not square.get_tile():
                tile.set_last_played()
                square.set_tile(tile)
                self.last_played_tiles.append(tile)

    def reset_last_play_cue(self):
        while self.last_played_tiles:
            tile = self.last_played_tiles.pop()
            tile.reset_last_played()

    def render_board(self):
        board_str = '\r'

        def horizontal_index():
            index_str = '  '
            for i in range(Board.BOARD_DIMENSIONS):
                index_str += '  ' + str(i % 10) + ' '
            index_str += '\n'
            return index_str

        def horizontal_line():
            return '  ' + '\u251C' + '\u2500' * 3 + ('\u253C' + '\u2500'*3) * (Board.BOARD_DIMENSIONS - 1) + '\u2524' + '\n'

        def top_line():
            return '  ' + '\u250C' + '\u2500' * 3 + ('\u252C' + '\u2500'*3) * (Board.BOARD_DIMENSIONS - 1) + '\u2510' + '\n'

        def bottom_line():
            return '  ' + '\u2514' + '\u2500' * 3 + ('\u2534' + '\u2500'*3) * (Board.BOARD_DIMENSIONS - 1) + '\u2518' + '\n'

        board_str += horizontal_index()
        board_str += top_line()
        for index, row in enumerate(self.board):
            if 0 < index < 15:
                board_str += horizontal_line()
            board_str += (str(index % 10) + ' \u2502' + '\u2502'.join([square.visual_repr() for square in row]) + '\u2502 ' + str(index % 10) + '\n')
        board_str += bottom_line()
        board_str += horizontal_index()
        return board_str

    def visual_repr(self):
        return [[square.visual_repr() for square in row] for row in self.board]

    def get_board_arr(self):
        return self.board

    def transpose_board(self):
        self.board = list(zip(*self.board))
        for row in self.board:
            for square in row:
                square.transpose_square()

    def get_adjacent_square(self, square, direction):
        delta = self.ADJACENT_DIRECTIONS[direction]

        new_coord = (square.get_coord().y + delta[0], square.get_coord().x + delta[1])
        if 0 <= new_coord[0] < Board.BOARD_DIMENSIONS and 0 <= new_coord[1] < Board.BOARD_DIMENSIONS:
            new_square = self.get_square(new_coord)
        else:
            new_square = Board.OFF_BOARD_SQUARE

        return new_square

    def get_adjacent_squares(self, square):
        up_square = self.get_adjacent_square(square, "above")
        down_square = self.get_adjacent_square(square, "below")
        left_square = self.get_adjacent_square(square, "left")
        right_square = self.get_adjacent_square(square, "right")

        return Adjacent_Squares(up_square, down_square, left_square, right_square)

    def __getitem__(self, item):
        return self.board[item]

    def __len__(self):
        return len(self.board)

    def __eq__(self, other):
        return isinstance(other, Board) and all(self.board[i] == other.board[i] for i in range(max(len(self.board), len(other.board))))
