import socketio
import sys
import argparse


MESSAGE_LINE_BUFFER = {'max': 5, 'current': -1, 'offset': 11}

# TODO add argparser
# user_config = {'username': sys.argv[1], 'room': None}

# if len(sys.argv) >= 3:
#     user_config['room'] = sys.argv[2]
# if len(sys.argv) == 3:
#     user_config['socket'] = sys.argv[3]
# else:
#     user_config['socket'] = 'http://localhost:5000'



parser = argparse.ArgumentParser(description='Run a network Scrabble game')

parser.add_argument('username',
                       type=str,
                       help='player name to use when connecting to a game')

parser.add_argument('-r',
                    '--room',
                    action='store',
                    help='to connect to an existing game room')

parser.add_argument('-a',
                    '--address',
                    action='store',
                    default='http://localhost:5000',
                    help='optional socket address of game host; ip:port')

user_config = parser.parse_args()

sio = socketio.Client()

from pyscrabble.client.client_interface import ClientInterface

tty_printer = ClientInterface()

from .events import *
