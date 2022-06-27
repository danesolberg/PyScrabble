import eventlet

eventlet.monkey_patch()

import os
import redis
from flask import Flask
from flask_socketio import SocketIO


REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_URL = f"redis://{REDIS_HOST}"

socketio = SocketIO()
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0)

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
                      message_queue=REDIS_URL,
                      logger=False,
                      engineio_logger=False
                      )

    # register websocket events
    from . import events

    return app
