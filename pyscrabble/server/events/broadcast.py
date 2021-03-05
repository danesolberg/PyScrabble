from flask_socketio import emit

from ..application import socketio


@socketio.on('broadcast')
def broadcast(data):
    emit('message', {'message': data['message']}, broadcast=True)
