from flask_socketio import send, leave_room
from flask import request

from ..application import socketio, redis_client
from ..utilities import handle_leave_room, set_skip_timeout_if_current_player


@socketio.event
def leave(data):
    username = data['username']
    room = data['room']
    if redis_client.sismember('rooms', room):
        leave_room(room)
        handle_leave_room(room, request.sid, username)
        set_skip_timeout_if_current_player(room, username, 0)
        send(username + ' has left the room.', room=room)
