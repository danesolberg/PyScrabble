from .message import message
from ..configs import sio, tty_printer


@sio.on('bad move')
def bad_move(error):
    message(error)
