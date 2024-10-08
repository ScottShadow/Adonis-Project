from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('message')
def handle_message(data):
    print(f"Received message: {data}")
    send(data, broadcast=True)  # Broadcast message to all clients


if __name__ == '__main__':
    socketio.run(app, debug=True)
