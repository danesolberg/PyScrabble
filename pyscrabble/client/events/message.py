from ..configs import sio, tty_printer, MESSAGE_LINE_BUFFER


MAX_BUFFER = MESSAGE_LINE_BUFFER['max']
BUFFER_OFFSET = MESSAGE_LINE_BUFFER['offset']


@sio.event
def message(data):
    if isinstance(data, dict):
        message = data['message']
    else:
        message = data

    MESSAGE_LINE_BUFFER['current'] = (MESSAGE_LINE_BUFFER['current'] + 1) % MAX_BUFFER
    row = MESSAGE_LINE_BUFFER['current'] + BUFFER_OFFSET
    tty_printer.clear_between(row, MAX_BUFFER + BUFFER_OFFSET)
    tty_printer.render_str(row, 0, message)
