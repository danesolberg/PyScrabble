from flask_socketio import emit

from ..application import socketio


@socketio.on('room message')
def room_message(data):
    emit('message', {'message': data['message']}, room=data['room'])
