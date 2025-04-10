from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.room import Room, UserSubscription, RoomTypes
from models.user import User
from models.message import Message
from models.models_helper import get_db_session
from api.v2.app import logging
from flask_socketio import emit
from api.v2.views.app_sockets import socketio


def assign_user_to_global_room(user_id):
    with get_db_session() as session:
        # Check if the global room exists
        # print(f"[DEBUG ASSIGN GLOBAL] global room checking")
        global_room = session.query(Room).filter_by(name="Global").first()
        # print(f"[DEBUG ASSIGN GLOBAL] global room checking finished")
        logging.info("Global room: %s", global_room)

        # If the global room doesn't exist, create it
        if not global_room:
            logging.info(f"[DEBUG ASSIGN GLOBAL] global room doesnt exist")
            logging.debug("Global room doesn't exist, creating it")
            global_room = Room(name="Global", is_dm=False,
                               type=RoomTypes.CHAT)
            session.add(global_room)
            session.commit()
            logging.debug("Global room created: %s", global_room)
        logging.info(f"[DEBUG ASSIGN GLOBAL] global room exist")
        # Check if user is already subscribed to the global room
        existing_subscription = session.query(UserSubscription).filter_by(
            user_id=user_id,
            room_id=global_room.id
        ).first()

        # Add user to the global room if they're not already subscribed
        if not existing_subscription:
            logging.debug("Adding user to global room: %s", global_room)
            subscription = UserSubscription(
                user_id=user_id,
                room_id=global_room.id,
                is_muted=False
            )
            session.add(subscription)
            session.commit()
            logging.debug("User added to global room: %s", global_room)

        logging.debug(
            "Returning global room with user included: %s - %s", global_room,
            user_id)


def create_user_circle(user_id):
    try:
        with get_db_session() as session:
            user_circle = session.query(Room).filter_by(
                name=f"circle_{user_id}").first()

            if not user_circle:
                user_room = Room(
                    name=f"circle_{user_id}", type=RoomTypes.CIRCLE)
                session.add(user_room)
                session.commit()
                logging.info(
                    f"User circle created successfully for user {user_id}")
                return True

            logging.info(f"User circle already exists for user {user_id}")
            return True

    except SQLAlchemyError as e:
        logging.error(
            f"Database error while creating user circle for {user_id}: {str(e)}")
        session.rollback()  # Rollback changes on failure
        return False

    except Exception as e:
        logging.error(
            f"Unexpected error while creating user circle for {user_id}: {str(e)}")
        return False


def find_dm_room(session: Session, user1_id, user2_id):
    # Subquery: group subscriptions for the two users by room_id
    subquery = (
        session.query(
            UserSubscription.room_id,
            func.count(UserSubscription.user_id).label("member_count")
        )
        .filter(UserSubscription.user_id.in_([user1_id, user2_id]))
        .group_by(UserSubscription.room_id)
        .subquery()
    )

    # Join the subquery with Room to check the is_dm flag and that exactly 2 members exist
    room = (
        session.query(Room)
        .join(subquery, Room.id == subquery.c.room_id)
        .filter(Room.is_dm == True, subquery.c.member_count == 2)
        .first()
    )

    return room
