from flask import request
from flask_socketio import send

from ..application import socketio, redis_client
from ..utilities import handle_leave_room


@socketio.event
def disconnect():
    sid = request.sid
    user_rooms = redis_client.smembers('user:' + sid + ':rooms')
    for room in user_rooms:
        room = room.decode('utf-8')
        username = redis_client.hget('users:usernames', sid + ':' + room).decode('utf-8')
        handle_leave_room(room, sid)
        send(username + ' has left room %s.' % room, room=room)
