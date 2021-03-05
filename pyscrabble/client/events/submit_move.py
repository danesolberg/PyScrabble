from ..configs import sio, tty_printer, user_config


# TODO spawn a new thread to handle inputs?
from ..utilities import main_thread_alive


@sio.on('your move')
def submit_move():
    # tty_printer.render_str(55, 0, 'Direction to place word: (d/r): ')
    while True:
        while True:
            if not main_thread_alive():
                return
            tty_printer.render_str(53, 0, 'Direction to place word: (d/r): ')
            direction = tty_printer.get_key()
            if direction in ['d', 'r']:
                break
        while True:
            if not main_thread_alive():
                return
            tty_printer.render_str(53, 0, 'Coordinate to place word (row,column): ')
            location = tty_printer.get_str()
            try:
                location = location.split(',')
                location = tuple(map(int, [location[0], location[1]]))
                break
            except (ValueError, IndexError):
                pass
        tty_printer.render_str(53, 0, 'Enter word to play: ')
        word = tty_printer.get_str().upper()
        break

    sio.emit('submit move', {'location': location, 'direction': direction, 'word': word, 'room': user_config['room']})
