import time
import pickle
from operator import attrgetter

from flask_socketio import send, emit

from pyscrabble.game_engine.exceptions import TurnSkippedException

from .application import redis_client


def handle_join_room(room, sid, username):
    redis_client.sadd('room:' + room + ':members', username)
    redis_client.sadd('room:' + room + ':active_members', username)
    redis_client.sadd('connection:' + sid + ':rooms', room)
    redis_client.hset('player:connection', username + ':' + room, sid)
    redis_client.hset('connection:player', sid + ':' + room, username)
    update_players(room)


def handle_leave_room(room, sid, username):
    redis_client.srem('room:' + room + ':active_members', username)
    redis_client.srem('connection:' + sid + ':rooms', room)
    redis_client.hdel('player:connection', username + ':' + room, sid)
    redis_client.hdel('connection:player', sid + ':' + room, username)
    if redis_client.scard('room:' + room + ':active_members') == 0:
        cleanup_state_on_room_end(room)
    update_players(room)


def cleanup_state_on_room_end(room):
    redis_client.srem('rooms:global', room)
    redis_client.delete('room:' + room + ":members")
    redis_client.delete('room:' + room + ":active_members")
    redis_client.hdel('rooms:inplay', room)

def set_skip_timeout_if_current_player(room, username, timeout):
    def begin_skip_timeout():
        send('%s will be skipped in %s seconds.' % (username, timeout), room=room)
        set_skip_flag(room, username)
        time.sleep(timeout)
        if get_skip_flag(room, username):
            process_next_turn(room, True)
            clear_skip_flag(room, username)

    if room_is_in_play(room):
        game = get_game_state(room)
        current_player_username = game.get_current_player().get_name()
        if username == current_player_username :
            begin_skip_timeout()


def get_game_state(room):
    return pickle.loads(redis_client.get('game:room:' + room))


def set_game_state(room, game):
    return redis_client.set('game:room:' + room, pickle.dumps(game)) == 1


def handle_start_game(room):
    if redis_client.hexists('rooms:inplay', room):
        redis_client.hset('rooms:inplay', room, '1')
    update_board(room)
    update_racks(room)

# implement this in a Game subclass
def process_next_turn(room, retry=False):
    # TODO check for end state or skip turns
    game = get_game_state(room)
    if game.is_end_state():
        if game.end_state is game.OUT_OF_MOVES_ENDING:
            game.process_out_of_moves_ending()
        elif game.end_state is game.OUT_OF_TILES_ENDING:
            game.process_out_of_tiles_ending()
        return

    if retry:
        username = game.get_current_player().get_name()
    else:
        username = game.get_next_player().get_name()
    game.turn += 1
    skipped = False
    # allow user to skip turn also
    try:
        if not redis_client.sismember('room:' + room + ':active_members', username):
            send('%s is disconnected.' % username, room=room)
            game.skip_turn()
        else:
            sid = get_sid(room, username)
            # not the right place for this
            game.skips = 0
            emit('your move', room=sid)
    except TurnSkippedException:
        send('%s skips their turn.' % username, room=room)
        skipped = True

    set_game_state(room, game)
    update_board(room)
    update_racks(room)
    update_header(room)

    if skipped:
        process_next_turn(room)


def update_board(room):
    game = get_game_state(room)
    board = game.board.visual_repr()
    emit('update board', board, room=room)


def update_rack(room, sid, username):
    game = get_game_state(room)
    emit('update rack', game.get_player(username).rack.get_rack_str(), room=sid)


def update_racks(room):
    game = get_game_state(room)
    active_members = set([username.decode('utf-8') for username in redis_client.smembers('room:' + room + ':active_members')])
    for player in game.get_all_players():
        username = player.get_name()
        if username in active_members:
            sid = get_sid(room, username)
            emit('update rack', game.get_player(username).rack.get_rack_str(), room=sid)


def update_players(room):
    usernames = [username.decode('utf-8') for username in redis_client.smembers('room:' + room + ':active_members')]
    emit('update players', {'players': usernames}, room=room)


def update_header(room):
    game = get_game_state(room)
    emit('update header', {
        'turn_number': game.get_turn(),
        'current_player': game.get_current_player().get_name(),
        'scores': {plr.get_name(): plr.get_score()
                   for plr in sorted(game.get_all_players(), key=attrgetter('name'))},
        'remaining_tiles': len(game.get_bag())
    }, room=room)


def get_username(room, sid):
    return redis_client.hget('connection:player', sid + ':' + room).decode('utf-8')


def get_sid(room, username):
    return redis_client.hget('player:connection', username + ':' + room).decode('utf-8')


def room_is_in_play(room):
    return redis_client.hget('rooms:inplay', room) == b'1'


def user_is_room_member(room, username):
    return redis_client.sismember('room:' + room + ':members', username)


def user_is_room_active_member(room, username):
    return redis_client.sismember('room:' + room + ':active_members', username)


def set_skip_flag(room, username):
    return redis_client.sadd('skip:user', username + ':' + room)


def clear_skip_flag(room, username):
    return redis_client.srem('skip:user', username + ':' + room)


def get_skip_flag(room, username):
    return redis_client.sismember('skip:user', username + ':' + room)
    