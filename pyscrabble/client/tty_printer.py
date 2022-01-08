import curses
import sys
import signal
from functools import wraps
import threading
import time

from .utilities import main_thread_alive

def blink(blink_bool):
    while True:
        time.sleep(0.5)
        blink_bool[0] = not blink_bool[0]


class TtyPrinter():
    MIN_HEIGHT = 60
    MIN_WIDTH = 90

    def __init__(self, stdscr=None):
        if stdscr is not None:
            self.init_scr(stdscr)
        self.lock = threading.Lock()
        self.blink = [False]

        threading.Thread(target=blink, name="CursorBlinkThread", args=([self.blink]), daemon=True).start()

    def init_scr(self, stdscr):
        stdscr.scrollok(False)
        curses.echo()
        curses.curs_set(True)
        stdscr.keypad(True)
        stdscr.leaveok(True)
        stdscr.immedok(False)
        stdscr.nodelay(True)

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

        TtyPrinter.set_cursor_visibility(False)

    def catch_sigint(func):
        @wraps(func)
        def func_wrapper(inst, *args, **kwargs):
            if not curses.isendwin():
                return func(inst, *args, **kwargs)
        return func_wrapper

    @staticmethod
    def set_cursor_visibility(vis_bool):
        curses.curs_set(vis_bool)

    # TODO change all to addnstr() with window width so avoid overflow errors
    @catch_sigint
    def render_str(self, y, x, text):
        self.lock.acquire()
        cursor_loc = self.get_cursor_yx()
        self.stdscr.addstr(y, x, text)
        self.stdscr.clrtoeol()
        self.set_cursor_yx(*cursor_loc)
        self.refresh()
        self.lock.release()

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
    def get_input(self, y, x, prompt_text):
        d = ''
        self.lock.acquire()
        self.stdscr.addstr(y, x, prompt_text)
        self.stdscr.clrtoeol()

        while main_thread_alive():
            cursor = '\u2581' if self.blink[0] else " "
            self.stdscr.addstr(y, x, (prompt_text + d + cursor).encode('utf-8'))
            self.set_cursor_yx(y, x + len(prompt_text) + len(d))
            self.refresh()
            k = self.stdscr.getch()
            if k > -1:
                c = chr(k)
                if c == '\n':
                    break
                elif c:
                    d = d + c
            self.lock.release()
            time.sleep(0.01)
            self.lock.acquire()

        if self.lock.locked():
            self.lock.release()
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
    def get_key_no_echo(self, y, x):
        curses.noecho()
        k = self.get_key(y, x)
        curses.echo()
        return k

    def get_cursor_yx(self):
        return self.stdscr.getyx()

    def set_cursor_yx(self, y, x):
        self.stdscr.move(y, x)
        self.refresh()

    def _safe_close(self, signal, frame):
        self.render_str(46, 0, 'Exiting game...')
        self.erase()
        curses.endwin()
        print('GAME END')
        sys.exit(0)
