from app import create_app

app, socketio = create_app()

if __name__ == "__main__":
    # Run the application with SocketIO support
    socketio.run(app, debug=True)
