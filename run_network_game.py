import curses
from pyscrabble.client.utilities import main_thread_alive

from pyscrabble.client.configs import tty_printer, sio


def run(stdscr):
    tty_printer.init_scr(stdscr)
    sio.connect('http://localhost:5000')
    sio.wait()


if __name__ == '__main__':
    curses.wrapper(run)
