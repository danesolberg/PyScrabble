import curses
import sys
import signal
from functools import wraps


class TtyPrinter():
    MIN_HEIGHT = 60
    MIN_WIDTH = 90

    def __init__(self, stdscr=None):
        if stdscr is not None:
            self.init_scr(stdscr)

    def init_scr(self, stdscr):
        stdscr.scrollok(False)
        curses.echo()
        curses.curs_set(True)
        stdscr.keypad(True)
        stdscr.leaveok(False)
        stdscr.immedok(False)
        stdscr.timeout(20)

        height, width = stdscr.getmaxyx()
        while height < self.MIN_HEIGHT or width < self.MIN_WIDTH:
            stdscr.addnstr(0, 0, "...", width)
            height, width = stdscr.getmaxyx()
            stdscr.addnstr(0, 0,
                           f"Terminal must be at least {self.MIN_HEIGHT} lines and {self.MIN_WIDTH} columns." +
                           f"Currently {height} x {width}.",
                           width
                          )
            stdscr.getch()
        stdscr.erase()

        self.stdscr = stdscr
        signal.signal(signal.SIGINT, self._safe_close)

    def catch_sigint(func):
        @wraps(func)
        def func_wrapper(inst, *args, **kwargs):
            if not curses.isendwin():
                return func(inst, *args, **kwargs)
        return func_wrapper

    # TODO change all to addnstr() with window width so avoid overflow errors
    @catch_sigint
    def render_str(self, *args):
        self.stdscr.addstr(*args)
        self.stdscr.clrtoeol()
        self.refresh()

    @catch_sigint
    def render_line(self):
        self.stdscr.addstr("\n")
        self.refresh()

    @catch_sigint
    def refresh(self):
        self.stdscr.refresh()

    def erase(self):
        self.stdscr.erase()

    def clear_line(self, row):
        pos = self.stdscr.getyx()
        self.stdscr.move(row, 0)
        self.stdscr.clrtoeol()
        self.stdscr.move(*pos)
        self.refresh()

    def clear_between(self, start, end):
        pos = self.stdscr.getyx()
        for row in range(start, end+1):
            self.stdscr.move(row, 0)
            self.stdscr.clrtoeol()
        self.stdscr.move(*pos)
        self.refresh()

    def clear_to_bottom(self):
        self.stdscr.clrtobot()
        self.refresh()

    @catch_sigint
    def get_str(self):
        d = ''

        while True:
            c = self.get_key()
            if c == '\n':
                break
            elif c:
                d = d + c
        return d

    @catch_sigint
    def get_char(self):
        return self.stdscr.getch()

    @catch_sigint
    def get_key(self):
        try:
            k = self.stdscr.getkey()
        except:
            return
        return k

    @catch_sigint
    def get_key_no_echo(self):
        curses.noecho()
        k = self.get_key()
        curses.echo()
        return k

    def get_cursor_yx(self):
        return self.stdscr.getyx()

    def _safe_close(self, signal, frame):
        self.render_str(46, 0, 'Exiting game...')
        self.erase()
        curses.endwin()
        print('GAME END')
        sys.exit(0)
