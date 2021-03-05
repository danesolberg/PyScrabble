import threading


def render_board(board):
    BOARD_DIMENSIONS = len(board)
    board_str = '\r'

    def horizontal_index():
        index_str = '  '
        for i in range(BOARD_DIMENSIONS):
            index_str += '  ' + str(i % 10) + ' '
        index_str += '\n'
        return index_str

    def horizontal_line():
        return '  ' + '\u251C' + '\u2500' * 3 + ('\u253C' + '\u2500' * 3) * (
                    BOARD_DIMENSIONS - 1) + '\u2524' + '\n'

    def top_line():
        return '  ' + '\u250C' + '\u2500' * 3 + ('\u252C' + '\u2500' * 3) * (
                    BOARD_DIMENSIONS - 1) + '\u2510' + '\n'

    def bottom_line():
        return '  ' + '\u2514' + '\u2500' * 3 + ('\u2534' + '\u2500' * 3) * (
                    BOARD_DIMENSIONS - 1) + '\u2518' + '\n'

    board_str += horizontal_index()
    board_str += top_line()
    for index, row in enumerate(board):
        if 0 < index < 15:
            board_str += horizontal_line()
        board_str += (str(index % 10) + ' \u2502' + '\u2502'.join(
            [square for square in row]) + '\u2502 ' + str(index % 10) + '\n')
    board_str += bottom_line()
    board_str += horizontal_index()
    return board_str


def render_rack(rack):
    return ", ".join(rack)


def main_thread_alive():
    return threading.main_thread().is_alive()
