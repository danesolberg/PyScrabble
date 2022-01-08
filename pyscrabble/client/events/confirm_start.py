from ..configs import sio, tty_printer, user_config
from ..utilities import main_thread_alive


COMMAND_LINE_ROW = 53
START_TEXT = 'Enter (s) to start game once all players have entered lobby:'

@sio.on('confirm start')
def confirm_start():
    tty_printer.render_str(COMMAND_LINE_ROW, 0, START_TEXT)
    while True:
        if not main_thread_alive():
            return
        key = tty_printer.get_input(COMMAND_LINE_ROW, 0, START_TEXT)
        if key == 's':
            break
        else:
            continue
    tty_printer.clear_line(COMMAND_LINE_ROW)
    sio.emit('start', {'room': user_config['room']})
