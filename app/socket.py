from flask_socketio import SocketIO

def init_socketio_events(socketio: SocketIO):
    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    @socketio.on('message')
    def handle_message(message):
        print(f'Received message: {message}')
        # Optionally emit a response
        socketio.send('Message received')

# Initialize events in your app
def init_app():
    from flask import Flask
    from flask_socketio import SocketIO

    app = Flask(__name__)
    socketio = SocketIO(app)

    # Initialize SocketIO events
    init_socketio_events(socketio)

    return app, socketio

if __name__ == "__main__":
    app, socketio = init_app()
    socketio.run(app, debug=True)
