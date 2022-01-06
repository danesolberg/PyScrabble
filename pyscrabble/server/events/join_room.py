from flask_socketio import send, emit, join_room
from flask import request

from ..application import socketio, redis_client
from ..utilities import handle_join_room, get_game_state, set_game_state, room_is_in_play, user_is_room_active_member, user_is_room_member


@socketio.event
def join(data):
    username = data['username']
    room = data['room']
    if not redis_client.sismember('rooms:global', room):
        send('Room %s does not exist.' % room)
        return
    elif not redis_client.scard('room:' + room + ':members') < 4:
        send('Room %s already full.' % room)
        return
    elif user_is_room_active_member(room, request.sid):
        send('%s is already connected to room %s', username, room)
        return
    elif room_is_in_play(room):
        if not user_is_room_member(room, request.sid):
            send('Game in progress. Room %s is closed.' % room)
            return
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
