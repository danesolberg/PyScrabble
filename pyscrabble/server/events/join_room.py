from flask import request
from flask_socketio import emit, join_room, send

from ..application import redis_client, socketio
from ..utilities import (clear_skip_flag, get_game_state, handle_join_room, room_is_in_play,
                         set_game_state, update_board, update_header, update_racks, user_is_room_active_member,
                         user_is_room_member)


@socketio.event
def join(data):
    username = data['username']
    room = data['room'].lower()

    if not redis_client.sismember('rooms:global', room):
        send('Room %s does not exist.' % room)
        return
    elif not redis_client.scard('room:' + room + ':members') < 4:
        send('Room %s already full.' % room)
        return
    elif user_is_room_active_member(room, username):
        send('%s is already connected to room %s' % (username, room))
        return
    elif room_is_in_play(room) or user_is_room_member(room, username):
        if not user_is_room_member(room, username):
            send('Game in progress. Room %s is closed.' % room)
            return
    else:
        try:
            game = get_game_state(room)
            game.add_player(username, False)
            set_game_state(room, game)
        except Exception as e:
            raise e

    join_room(room)
    clear_skip_flag(room, username)
    handle_join_room(room, request.sid, username)
    emit('joined', {'message': username + ' has entered room ' + room, 'room': room}, room=room)
    game = get_game_state(room)
    if game.get_current_player() and game.get_current_player().get_name() == username:
        update_board(room)
        update_racks(room)
        update_header(room)
        emit('your move', room=request.sid)
