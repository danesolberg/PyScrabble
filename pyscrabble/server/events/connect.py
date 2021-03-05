from flask_socketio import emit

from ..application import socketio


@socketio.event
def connect():
    emit('message', {'message': 'Connected'})
