from flask import request
from flask_socketio import send

from ..application import socketio, redis_client
from ..utilities import handle_leave_room, get_username, set_skip_timeout_if_current_player


@socketio.event
def disconnect():
    sid = request.sid
    connection_rooms = redis_client.smembers('connection:' + sid + ':rooms')
    for room in connection_rooms:
        room = room.decode('utf-8')
        username = get_username(room, sid)
        handle_leave_room(room, sid, username)
        send(username + ' has disconnected', room=room)
        set_skip_timeout_if_current_player(room, username, 15)
