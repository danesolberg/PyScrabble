import curses

from pyscrabble.client.configs import tty_printer, sio, user_config


def run(stdscr):
    tty_printer.init_scr(stdscr)
    sio.connect(user_config.address)
    sio.wait()


if __name__ == '__main__':
    curses.wrapper(run)
