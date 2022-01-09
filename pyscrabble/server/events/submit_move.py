from flask_socketio import emit
from flask import request

from ..application import socketio
from ..utilities import get_game_state, set_game_state, get_sid, process_next_turn
from pyscrabble.game_engine.word import Word


@socketio.on('submit move')
def submit_move(data):
    room = data['room']
    word = data['word']
    location = data['location']
    direction = data['direction']

    game = get_game_state(data['room'])
    current_player_username = game.get_current_player().get_name()
    current_player_sid = get_sid(room, current_player_username)
    if current_player_sid == request.sid:
        try:
            play = Word(game, word, location, direction)
            game.place_move(play)
        except Exception as e:
            emit('bad move', str(e), room=current_player_sid)
            emit('your move', room=current_player_sid)
            return

        game.current_player.rack.refill_tiles_in_rack()
        set_game_state(room, game)

        emit('word played', {'username': current_player_username,
                             'word': word,
                             'score': play.get_score()},
             room=data['room'])
             
        process_next_turn(room)


