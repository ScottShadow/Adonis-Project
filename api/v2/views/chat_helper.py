from models.room import Room
from models.user import User
from models.message import Message
from models.models_helper import get_db_session
from api.v2.app import logging
from flask_socketio import emit
from api.v2.views.app_sockets import socketio


def assign_user_to_global_room(user):
    with get_db_session() as session:
        # Check if the global room exists
        global_room = session.query(Room).filter_by(name="Global").first()
        user = session.query(User).filter_by(id=user.id).first()
        logging.debug("Global room: %s", global_room)
        # If the global room doesn't exist, create it
        if not global_room:
            logging.debug("Global room doesn't exist, creating it")
            global_room = Room(name="Global", is_dm=False)
            session.add(global_room)

            """creation_msg = Message(room_id=global_room.id, user_id=user.id,
                                   content=f"Group chat room created!")
            session.add(creation_msg)
            session.commit()
            pay_load = {"username": user.username,
                        "message": "Room Created", "created_at": creation_msg.created_at.strftime('%Y-%m-%d %H:%M:%S')}
            # Emit the message to everyone in the room
            socketio.emit('message', pay_load, room=room_id)"""
            session.commit()
            logging.debug("Global room created: %s", global_room)
        # Add user to the global room if they're not already in it
        if global_room not in user.rooms:
            logging.debug("Adding user to global room: %s", global_room)
            user.rooms.append(global_room)
            # welcome_msg = Message(room_id=global_room.id, user_id=user.id,
            #                      content = f"{user.username} has joined the room!")
            # session.add(welcome_msg)
            session.commit()
            logging.debug("User added to global room: %s", global_room)

        logging.debug(
            "Returning global room with user included: %s - %s", global_room, user.username)
