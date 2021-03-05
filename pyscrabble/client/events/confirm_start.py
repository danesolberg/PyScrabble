from ..configs import sio, tty_printer, user_config
from ..utilities import main_thread_alive


@sio.on('confirm start')
def confirm_start():
    command_line = 18
    while True:
        if not main_thread_alive():
            return
        tty_printer.render_str(command_line, 0, 'Press (s) to start game once all players have entered lobby: ')
        key = tty_printer.get_key_no_echo()
        if key == 's':
            break
        else:
            continue
    tty_printer.clear_line(command_line)
    sio.emit('start', {'room': user_config['room']})
