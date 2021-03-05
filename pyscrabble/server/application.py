import eventlet

eventlet.monkey_patch()

import redis
from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()
redis_client = redis.Redis(host='localhost', port=6379, db=0)


def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'secret!'

    # CORS(app)
    with app.app_context():
        from .routes import api as api_blueprint
        app.register_blueprint(api_blueprint)

    socketio.init_app(app,
                      async_mode='eventlet',
                      message_queue='redis://127.0.0.1:6379',
                      logger=False,
                      engineio_logger=False
                      )

    # register websocket events
    from . import events

    return app
