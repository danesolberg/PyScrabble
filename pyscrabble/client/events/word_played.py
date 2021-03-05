from .message import message
from ..configs import sio, tty_printer


@sio.on('word played')
def word_played(data):
    username = data['username']
    word = data['word']
    score = data['score']
    message(f"{username} played {word} for {score} points.")
