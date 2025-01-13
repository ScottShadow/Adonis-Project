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
from math import ceil

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
    user = request.current_user
    current_user_id = user.id

    # Pagination parameters
    page = int(request.args.get('page', 1))
    per_page = 8  # Number of users per page

    with get_db_session() as session:
        total_users = session.query(User).filter(
            User.id != current_user_id).count()
        total_pages = ceil(total_users / per_page)

        users = (
            session.query(User.id, User.username)
            .filter(User.id != current_user_id)
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

    return render_template(
        'people.html',
        users=users,
        current_page=page,
        total_pages=total_pages
    )


@chat_views.route('/start_dm/<user_id>', methods=['GET', 'POST'])
def start_dm(user_id):
    with get_db_session() as session:
        user = request.current_user  # Fetch current user
        if not user:
            logging.warning("Unauthorized access attempt for user")
            abort(404)

        current_user_id = user.id

        # Check if a room already exists for this DM
        room = (session.query(Room)
                .filter(Room.is_dm == True)
                .join(Room.users)
                .filter(User.id.in_([user_id, current_user_id]))
                .group_by(Room.id)
                .having(func.count(User.id) == 2)
                .first())

        # Fetch the other user
        other_user = session.query(User).filter_by(id=user_id).first()
        if not other_user:
            logging.warning(f"User with id {user_id} not found")
            abort(404)

        logging.info(
            f"[Start DM] Current user: {user.username}, Other user: {other_user.username}")

        if room is None:
            # Create new DM room
            room_name = f"DM between {user.username} and {other_user.username}"
            room = Room(name=room_name, is_dm=True)
            session.add(room)
            session.flush()

            # Add both users to the room
            room.users.append(user)
            room.users.append(other_user)
            session.flush()
            session.commit()

            logging.debug(f"DM room created: {room}")

        # Get all messages in the DM room
        messages = room.messages
        """messages = session.query(Message).options(
            joinedload(Message.user)).filter_by(room_id=room.id).all()"""

        formatted_messages = [{"username": message.user.username,
                               "content": message.content, "created_at": message.created_at}
                              for message in messages]

        return render_template('dm_page.html', room=room, messages=formatted_messages, user=user)


@chat_views.route('/dm/<room_id>', methods=['GET'])
def dm_page(room_id):
    with get_db_session() as session:
        room = session.query(Room).filter_by(id=room_id).first()

        if request.current_user not in room.users:
            return "Unauthorized", 403  # Ensure only the two users in the DM can access it

        messages = session.query(Message).options(
            joinedload(Message.user)).filter_by(room_id=room.id).all()
    return render_template('dm_page.html', room=room, messages=messages)
