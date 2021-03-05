from pyscrabble.server import create_app, socketio

service = create_app(debug=False)

if __name__ == "__main__":
    socketio.run(service)
