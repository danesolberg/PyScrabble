import pickle
from operator import attrgetter

from flask_socketio import send, emit

from .application import redis_client


def handle_join_room(room, sid, username):
    redis_client.sadd('room:' + room + ':members', sid)
    redis_client.sadd('user:' + sid + ':rooms', room)
    redis_client.hset('users:usernames', sid + ':' + room, username)
    update_players(room)


def handle_leave_room(room, sid):
    redis_client.srem('room:' + room + ':members', sid)
    redis_client.srem('user:' + sid + ':rooms', room)
    if redis_client.scard('room:' + room + ':members') == 0:
        redis_client.srem('rooms:global', room)
        redis_client.hdel('rooms:global:open', room)
    update_players(room)


def get_game_state(room):
    return pickle.loads(redis_client.get('game:room:' + room))


def set_game_state(room, game):
    return redis_client.set('game:room:' + room, pickle.dumps(game)) == 1


def handle_start_game(room):
    if redis_client.hexists('rooms:inplay', room):
        redis_client.hset('rooms:inplay', room, '1')
    update_board(room)
    update_racks(room)


def process_next_turn(room):
    # TODO check for end state or skip turns
    game = get_game_state(room)
    current_player_sid = game.get_next_player().get_name()
    game.turn += 1
    emit('your move', room=current_player_sid)
    set_game_state(room, game)
    update_board(room)
    update_rack(room, current_player_sid)
    update_header(room)


def update_board(room):
    game = get_game_state(room)
    emit('update board', game.board.visual_repr(), room=room)


def update_rack(room, sid):
    game = get_game_state(room)
    emit('update rack', game.get_player(sid).rack.get_rack_str(), room=sid)


def update_racks(room):
    game = get_game_state(room)
    for player in game.get_all_players():
        sid = player.get_name()
        emit('update rack', game.get_player(sid).rack.get_rack_str(), room=sid)


def update_players(room):
    sids = redis_client.smembers('room:' + room + ':members')
    usernames = []
    for sid in sids:
        sid = sid.decode('utf-8')
        username = redis_client.hget('users:usernames', sid + ':' + room)
        usernames.append(username.decode('utf-8'))
    emit('update players', {'players': usernames}, room=room)


def update_header(room):
    game = get_game_state(room)
    emit('update header', {
        'turn_number': game.get_turn(),
        'current_player': get_username(room, game.get_current_player().get_name()),
        'scores': {get_username(room, plr.get_name()): plr.get_score()
                   for plr in sorted(game.get_all_players(), key=attrgetter('name'))},
        'remaining_tiles': len(game.get_bag())
    }, room=room)


def get_username(room, sid):
    return redis_client.hget('users:usernames', sid + ':' + room).decode('utf-8')


def room_is_in_play(room):
    return redis_client.hget('rooms:inplay', room).decode('utf-8') == '1'
