from collections import namedtuple
from .square import Square
from .exceptions import CoordinateError


class Board:
    BOARD_WIDTH = 15
    BOARD_HEIGHT = 15
    Adjacent_Square = namedtuple('Adjacent_Square', ['left','right','up','down'])

    def __init__(self):
        self.board = [[Square((y,x)) for x in range(Board.BOARD_WIDTH)] for y in range(Board.BOARD_HEIGHT)]
        self.initialize_premium_squares()

    def get_square(self, coord):
        try:
            return self.board[coord[0]][coord[1]]
        except IndexError:
            raise CoordinateError(coord)

    def initialize_premium_squares(self):
        STARTING_SQUARE = (7,7)
        self.get_square(STARTING_SQUARE).set_text('*')
        self.get_square(STARTING_SQUARE).set_multiplier('DWS')

        PREMIUM_SQUARES = {
            'TWS': [(0,0), (7, 0), (14,0), (0, 7), (14, 7), (0, 14), (7, 14), (14,14)],
            'DWS': [(1,1), (2,2), (3,3), (4,4), (1, 13), (2, 12), (3, 11), (4, 10), (13, 1), (12, 2), (11, 3), (10, 4), (13,13), (12, 12), (11,11), (10,10)],
            'TLS': [(1,5), (1, 9), (5,1), (5,5), (5,9), (5,13), (9,1), (9,5), (9,9), (9,13), (13, 5), (13,9)],
            'DLS': [(0, 3), (0,11), (2,6), (2,8), (3,0), (3,7), (3,14), (6,2), (6,6), (6,8), (6,12), (7,3), (7,11), (8,2), (8,6), (8,8), (8, 12), (11,0), (11,7), (11,14), (12,6), (12,8), (14, 3), (14, 11)]
        }

        for multiplier in PREMIUM_SQUARES:
            for coord in PREMIUM_SQUARES[multiplier]:
                self.get_square(coord).set_text(multiplier)
                self.get_square(coord).set_multiplier(multiplier)

    def place_tiles_on_board(self, word):
        placement = word.get_word_placement()
        self.reset_last_play_cue()
        for pair in placement:
            square = pair[0]
            tile = pair[1]
            if not square.get_tile():
                square.set_tile(tile)
                square.get_tile().set_last_played()

    def reset_last_play_cue(self):
        for row in self.board:
            for square in row:
                if square.get_tile():
                    square.get_tile().reset_last_played()

    def visual_repr(self):
        board_str = '\r'

        def horizontal_index():
            index_str = '  '
            for i in range(Board.BOARD_WIDTH):
                index_str += '  ' + str(i % 10) + ' '
            index_str += '\n'
            return index_str

        def horizontal_line():
            return '  ' + '\u251C' + '\u2500'*3 + ('\u253C' + '\u2500'*3) * (Board.BOARD_WIDTH - 1) + '\u2524' + '\n'

        def top_line():
            return '  ' + '\u250C' + '\u2500'*3 + ('\u252C' + '\u2500'*3) * (Board.BOARD_WIDTH - 1) + '\u2510' + '\n'

        def bottom_line():
            return '  ' + '\u2514' + '\u2500'*3 + ('\u2534' + '\u2500'*3) * (Board.BOARD_WIDTH - 1) + '\u2518' + '\n'

        board_str += horizontal_index()
        board_str += top_line()
        for index, row in enumerate(self.board):
            if 0 < index < 15:
                board_str += horizontal_line()
            board_str += (str(index % 10) + ' \u2502' + '\u2502'.join([square.visual_repr() for square in row]) + '\u2502 ' + str(index % 10) + '\n')
        board_str += bottom_line()
        board_str += horizontal_index()
        return(board_str)

    def get_board_arr(self):
        return self.board

    def transpose_board(self):
        self.board = list(zip(*self.board))
        for row in self.board:
            for square in row:
                square.transpose_square()

    def get_offboard_square(self):
        return Square((-1,-1))

    def get_above_square(self, square):
        above_coord = square.get_coord()._replace(y = square.get_coord().y - 1)
        if 0 <= above_coord.y <= 14:
            above_square = self.get_square(above_coord)
        else:
            above_square = self.get_offboard_square()
        return above_square

    def get_below_square(self, square):
        below_coord = square.get_coord()._replace(y = square.get_coord().y + 1)
        if 0 <= below_coord.y <= 14:
            below_square = self.get_square(below_coord)
        else:
            below_square = self.get_offboard_square()
        return below_square

    def get_adjacent_square(self, square):
        left_coord = square.get_coord()._replace(x = square.get_coord().x - 1)
        if 0 <= left_coord.x <= 14:
            left_square = self.get_square(left_coord)
        else:
            left_square = self.get_offboard_square()

        right_coord = square.get_coord()._replace(x = square.get_coord().x + 1)
        if 0 <= right_coord.x <= 14:
            right_square = self.get_square(right_coord)
        else:
            right_square = self.get_offboard_square()

        up_square = self.get_above_square(square)
        down_square = self.get_below_square(square)

        return self.Adjacent_Square(left_square,right_square,up_square,down_square)