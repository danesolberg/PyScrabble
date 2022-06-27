from pyscrabble.server import create_app, socketio

service = create_app(debug=True)

if __name__ == "__main__":
    socketio.run(service, host='0.0.0.0', port=5000)
