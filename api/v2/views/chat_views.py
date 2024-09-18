from api.v2.views import app_views
from flask import abort, jsonify, request, redirect, url_for, render_template, Blueprint
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from models.room import Room
from models.message import Message
from models.user import User
from models.base import SessionLocal
from models.models_helper import get_db_session
from api.v2.app import logging

# app = app_views

chat_views = Blueprint("chat_views", __name__, url_prefix="/api/v2")


@chat_views.route('/global_chat')
def global_chat():
    with get_db_session() as session:
        user = request.current_user  # Assuming you have a function to get the current user
        if not user:
            logging.warning(
                "Unauthorized access attempt for user")
            abort(404)
        # Fetch the global room
        global_room = session.query(Room).filter_by(name="Global").first()

        if not global_room:
            global_room = Room(name="Global", is_dm=False)
            session.add(global_room)
            session.commit()
            logging.debug("Global room created: %s", global_room)

        # Get all messages in the global room ordered
        messages = global_room.messages
        logging.debug("Global room messages: %s", messages)

        formatted_messages = [{"username": message.user.username,
                               "content": message.content, "created_at": message.created_at} for message in messages]
        return render_template('global_chat.html', room=global_room, messages=formatted_messages, user=user)


@chat_views.route('/people', methods=['GET'])
def people():
    users = []
    with get_db_session() as session:
        users = session.query(User).all()  # Fetch all users
    return render_template('people.html', users=users)


@chat_views.route('/start_dm/<user_id>', methods=['POST'])
def start_dm(user_id):
    try:
        logging.info(f"[Start DM] CHECKING")
        # Assuming you have the current user ID
        current_user = request.current_user
        logging.info(f"[Start DM] Current user: {current_user.username}")
        current_user_id = current_user.id

        with get_db_session() as session:
            # Check if a room already exists for this DM
            room = (session.query(Room)
                    .filter(Room.is_dm == True)
                    .join(Room.users)
                    .filter(User.id.in_([user_id, current_user_id]))
                    .group_by(Room.id)
                    .having(func.count(User.id) == 2)
                    .first())
            logging.info(f"[Start DM] Room: {room}")
            user = session.query(User).filter_by(id=user_id).first()
            logging.info(f"[Start DM] Other User: {user.username}")
            if room is None:
                # Create new DM room
                room_name = f"DM between {current_user.username} and {user.username}"
                room = Room(name=room_name, is_dm=True)
                session.add(room)
                session.commit()

                # Add both users to the room
                room.users.append(current_user)
                room.users.append(user)
                session.commit()
    except Exception as e:
        logging.error(f"Error in start_dm: {e}")
        return jsonify({"error": "An error occurred while starting the DM"}), 500
    # Redirect to the DM page for this room
    return redirect(url_for('chat_views.dm_page', room_id=room.id))


@chat_views.route('/dm/<room_id>', methods=['GET'])
def dm_page(room_id):
    with get_db_session() as session:
        room = session.query(Room).filter_by(id=room_id).first()

        if request.current_user not in room.users:
            return "Unauthorized", 403  # Ensure only the two users in the DM can access it

        messages = session.query(Message).options(
            joinedload(Message.user)).filter_by(room_id=room.id).all()
    return render_template('dm_page.html', room=room, messages=messages)
