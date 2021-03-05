import socketio
import sys


MESSAGE_LINE_BUFFER = {'max': 5, 'current': -1, 'offset': 11}

# TODO add argparser
user_config = {'username': sys.argv[1], 'room': None}

if len(sys.argv) == 3:
    user_config['room'] = sys.argv[2]

sio = socketio.Client()

from pyscrabble.client.client_interface import ClientInterface

tty_printer = ClientInterface()

from .events import *
