import uuid

from flask_socketio import emit, send
from flask import request

from .join_room import join
from ..application import socketio, redis_client
from ..utilities import set_game_state
from ...game_engine.game import Game


def gen_room():
    while True:
        room = uuid.uuid4().hex[:4].lower()
        if redis_client.sadd('rooms:global', room) == 1:
            redis_client.hset('rooms:inplay', room, '0')
            return room


@socketio.event
def create(data):
    username = data['username']
    room = gen_room()
    game = Game()
    set_game_state(room, game)
    send(username + ' has created room %s' % room)
    join({'username': username, 'room': room})
    emit('confirm start', room=request.sid)
