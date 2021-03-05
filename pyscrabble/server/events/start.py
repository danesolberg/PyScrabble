from flask_socketio import send

from ..application import socketio, redis_client
from ..utilities import handle_start_game, process_next_turn, room_is_in_play


@socketio.event
def start(data):
    room = data['room']
    if not redis_client.sismember('rooms:global', room):
        send('Room %s does not exist.' % room)

    if not room_is_in_play(room):
        handle_start_game(room)
        send('Game has started.', room=room)
        process_next_turn(room)

