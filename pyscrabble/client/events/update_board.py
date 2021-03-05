from ..configs import sio, tty_printer
from ..utilities import render_board


@sio.on('update board')
def update_board(board):
    tty_printer.render_str(18, 0, render_board(board).encode('utf-8'))
