from flask_socketio import send, emit, join_room
from flask import request

from ..application import socketio, redis_client
from ..utilities import handle_join_room, get_game_state, set_game_state, room_is_in_play


@socketio.event
def join(data):
    username = data['username']
    room = data['room']
    if not redis_client.sismember('rooms:global', room):
        send('Room %s does not exist.' % room)
    elif not redis_client.scard('room:' + room + ':members') < 4:
        send('Room %s already full.' % room)
    elif room_is_in_play(room):
        send('Room %s is closed.' % room)
    else:
        try:
            game = get_game_state(room)
            game.add_player(request.sid, False)
        except Exception as e:
            raise e

        join_room(room)
        handle_join_room(room, request.sid, username)

        set_game_state(room, game)
        emit('joined', {'message': username + ' has entered room ' + room, 'room': room}, room=room)
