import socketio
import sys


def get_username():
    if len(sys.argv) < 2 or (sys.argv[1] == "<your_name>"):
        return input("You forgot to provide a user name. Please try again...")
    if sys.argv[1].startswith("<") and sys.argv[1].endswith(">"):
        return sys.argv[1].replace("<", "").replace(">", "")
    return sys.argv[1]


MESSAGE_LINE_BUFFER = {"max": 5, "current": -1, "offset": 11}

# TODO add argparser
user_config = {"username": get_username(), "room": None}

if len(sys.argv) == 3:
    user_config["room"] = sys.argv[2]

sio = socketio.Client()

from pyscrabble.client.client_interface import ClientInterface

tty_printer = ClientInterface()

from .events import *
