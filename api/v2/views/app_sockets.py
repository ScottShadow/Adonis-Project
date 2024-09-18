from flask_socketio import join_room, leave_room, send, emit
from flask_socketio import SocketIO, send, emit, join_room
from flask import request, abort, session as flask_session
from models.user import User
from models.room import Room
from models.message import Message
from models.models_helper import get_db_session
from api.v2.app import logging
from datetime import datetime

socketio = SocketIO()


def initialize_socketio(app):
    """Initialize SocketIO with the Flask app"""
    socketio.init_app(app, cors_allowed_origins="*")


@socketio.on('join')
def on_join(data):
    room_id = data['room_id']
    # check_room_exists(room_id)
    join_room(room_id)
    username = flask_session['username']
    logging.info(f"User {username} joined room {room_id}")
    # send(username + ' has entered the room.', to=room_id)
    # emit('status', {
    #     'message': f'{username} has entered the room.', 'created_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}, room=room_id)


@socketio.on('connect')
def handle_connect():
    from api.v2.app import auth
    user = auth.current_user(request)  # Authenticate the user when connecting
    if user is None:
        return False  # Prevent the connection if the user is not authenticated
    flask_session['user_id'] = user.id
    flask_session['username'] = user.username
    print(f"User {user.username} connected")


@socketio.on('message')
def handle_message(data):
    try:
        with get_db_session() as session:
            room_id = data['room_id']

            # Retrieve user info from the Flask session
            user_id = flask_session.get('user_id')
            username = flask_session.get('username')

            if not user_id or not username:
                return emit('error', {'message': 'User not logged in'})

            message_content = data['message']

            # Save the message to the database
            message = Message(room_id=room_id, user_id=user_id,
                              content=message_content)
            session.add(message)
            session.commit()
            pay_load = {"username": username,
                        "message": message_content, "created_at": message.created_at.strftime('%Y-%m-%d %H:%M:%S')}
            # Emit the message to everyone in the room
            emit('message', pay_load, room=room_id)
    except Exception as e:
        logging.error(f"Error in handle_message: {e}")
        emit(
            'error', {'message': 'An error occurred while sending the message'})


@socketio.on('disconnect')
def on_disconnect():
    print(f'Client:{flask_session.get("username")} disconnected')
    logging.info(f"User {flask_session.get('username')} disconnected")


# Join DM Room

# Ensure only the two users in a DM room can join
@socketio.on('join_dm')
def handle_join_dm(data):
    with get_db_session() as session:
        room_id = data['room']
        room = session.query(Room).filter_by(id=room_id).first()
        user_id = flask_session.get('user_id')
        current_user = session.query(User).filter_by(id=user_id).first()
        # Check if the current user is in the room
        if current_user not in room.users:
            emit('status', {'msg': 'Unauthorized to join this room.'})
            return

        join_room(room_id)
        emit('status', {
            'msg': f'User {current_user.username} has entered the room.'}, room=room_id)


# Handle message sent by a user


@socketio.on('send_message')
def handle_send_message(data):
    room_id = data['room']
    content = data['content']

    with get_db_session() as session:
        user_id = flask_session.get('user_id')
        current_user = session.query(User).filter_by(id=user_id).first()
        # Save message to the database
        message = Message(
            room_id=room_id, user_id=current_user.id, content=content)
        session.add(message)
        session.commit()

        # Emit message to everyone in the room
        emit('receive_message', {
            'username': current_user.username,
            'content': content
        }, room=room_id)
