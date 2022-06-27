from ..configs import sio, user_config


@sio.event
def connect():
    username = user_config.username
    room = user_config.room
    if room is None:
        sio.emit('create', {'username': username})
    else:
        sio.emit('join', {'username': username, 'room': room})
