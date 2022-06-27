from ..configs import sio, tty_printer, user_config
from ..utilities import main_thread_alive


COMMAND_LINE_ROW = 53
DIRECTION_TEXT = 'Direction to place word: (d/r):'
COORD_TEXT = 'Coordinate to place word (row,column):'
WORD_TEXT = 'Enter word to play:'

@sio.on('your move')
def submit_move():
    while True:
        while True:
            if not main_thread_alive():
                return
            direction = tty_printer.get_input(COMMAND_LINE_ROW, 0, DIRECTION_TEXT)
            if direction in ['d', 'r']:
                break
        tty_printer.render_str(COMMAND_LINE_ROW, 0, COORD_TEXT)
        while True:
            if not main_thread_alive():
                return
            location = tty_printer.get_input(COMMAND_LINE_ROW, 0, COORD_TEXT)
            try:
                location = location.split(',')
                location = tuple(map(int, [location[0], location[1]]))
                break
            except (ValueError, IndexError):
                pass
        tty_printer.render_str(COMMAND_LINE_ROW, 0, WORD_TEXT)
        word = tty_printer.get_input(COMMAND_LINE_ROW, 0, WORD_TEXT).upper()
        break

    sio.emit('submit move', {'location': location, 'direction': direction, 'word': word, 'room': user_config.room})
