import curses
import sys

from .tty_printer import TtyPrinter
from .configs import MESSAGE_LINE_BUFFER, sio


class ClientInterface(TtyPrinter):
    def __init__(self, stdscr=None):
        super().__init__(stdscr)

    def init_scr(self, stdscr):
        super().init_scr(stdscr)
        self.render_labels()

    def render_labels(self):
        self.stdscr.addstr(0, 0, 'PyScrabble')
        self.stdscr.addstr(MESSAGE_LINE_BUFFER['offset'] - 1, 0, 'Messages')

    def _safe_close(self, signal, frame):
        self.render_str(46, 0, 'Exiting game...')
        self.erase()
        curses.endwin()
        sio.disconnect()
        sio.wait()
        curses.endwin()
        sys.exit(0)
