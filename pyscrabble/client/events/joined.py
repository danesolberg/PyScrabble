import sys

from ..configs import sio, user_config, tty_printer
from .message import message


@sio.on('joined')
def joined(data):
    user_config.room = data['room']
    message(data['message'])
