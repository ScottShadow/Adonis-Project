from datetime import datetime
from api.v2.views import log_views
from flask import request, jsonify, render_template, Blueprint, session as flask_session, url_for
from models.log import Log
from models.user import User
from models.interaction import Comment, Reaction
from api.v2.app import auth, logging
from models.models_helper import get_db_session
from flask import Flask, request, jsonify, Blueprint
from pywebpush import webpush, WebPushException
import json
import os
from models.room import UserSubscription, NotificationEvent, Room, RoomTypes, EventTypes, ActivityStatus
from sqlalchemy import func, and_
event_views = Blueprint('event_views', __name__, url_prefix="/api/v2")

VAPID_PRIVATE_KEY = os.getenv(
    'VAPID_PRIVATE_KEY', "zB14ov1Wq9DhNCP1wMyTSwPmPRA0uhrtoq_qz-pKmOk")
VAPID_PUBLIC_KEY = os.getenv(
    'VAPID_PUBLIC_KEY', "BGfJy7eJBCiUU37HZYmJ61nwD5qbZEQ0iwRXKeEecs7NkAroAFYrpu0svHj3e0w8vNvTrZxrwmQTIwlJ8dTiM0Y")
VAPID_CLAIMS = {
    "sub": os.getenv('VAPID_CLAIMS_SUB', "mailto:rudaseswascottmc@gmail.com"),
    "aud": os.getenv('VAPID_CLAIMS_AUD', "https://fcm.googleapis.com")
}

subscriptions = []  # Store user subscriptions


@event_views.route("/subscribe", methods=["POST"])
def subscribe():
    # Retrieve subscription data from the request
    subscription_data = request.json

    # For debugging/logging
    logging.info(f"Received push subscription: {subscription_data}")

    # Retrieve the current user's ID from the Flask session
    user_id = request.current_user.id
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401

    # Use your session manager to update the user record
    try:
        with get_db_session() as session:
            # Query the user by id
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return jsonify({"error": "User not found"}), 404

            # Store the subscription data as a JSON string.
            # (You may need to adjust the field length/type in your model if necessary.)
            user.push_subscription = json.dumps(subscription_data)

            # Commit the changes
            session.commit()

            return jsonify({"message": "Subscription saved!"}), 201

    except Exception as e:
        logging.error(f"Error saving subscription: {e}")
        return jsonify({"error": "Failed to save subscription"}), 500


def send_push_notification(sender_name, message_content, url, recipient_id):
    # make table and make it modular
    """
    Send a push notification to the given user containing the message content
    and sender name. The notification will contain a URL to the given endpoint.

    :param sender_name: The name of the user sending the message
    :param message_content: The content of the message
    :param url: The URL of the endpoint to navigate to when the notification is clicked
    :param recipient_id: The ID of the user to send the notification to
    """
    payload = {
        "title": f"New message from {sender_name}",
        "message": message_content,
        "url": url
    }

    with get_db_session() as session:
        # print(f"Sending push notification to user {recipient_id}")
        user = session.query(User).filter_by(id=recipient_id).first()
        if not user or not user.push_subscription:
            # print(f"No push subscription found for user {recipient_id}")
            return

        try:
            webpush(
                subscription_info=json.loads(user.push_subscription),
                data=json.dumps(payload),
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS
            )
            # print(f"Push notification sent to user {recipient_id}")

        except WebPushException as e:
            logging.error("WebPush failed:", e)


@event_views.route("/send_notification", methods=["POST"])
def send_notification():
    data = request.json
    required_fields = ["title", "message", "url", "room_id", "sender_id"]

    # Validate incoming data
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        NotificationService.notify_room(
            data["room_id"], data["sender_id"], data["message"], data["url"])
        return jsonify({"message": "Notification sent!"}), 200
    except Exception as e:
        logging.error(f"Error sending notification: {e}")
        return jsonify({"error": "Failed to send notification"}), 500


@event_views.route("/test", methods=["GET"])
def test():
    return render_template('test.html')


@event_views.route('/events/home', methods=['GET'], strict_slashes=False)
def home():
    return render_template('event_home.html')


class NotificationService:
    @staticmethod
    def notify_room(room_id, sender_id, message_content):
        """
        Notify all users in a room except the sender.
        """
        with get_db_session() as session:
            # Find the room name for the notification
            room = session.query(Room).filter_by(id=room_id).first()
            room_name = room.name if room else "the room"
            url = ""
            # Find all users in the room
            subscriptions = session.query(
                UserSubscription).filter_by(room_id=room_id).all()
            # Exclude sender
            user_ids = [
                sub.user_id for sub in subscriptions if sub.user_id != sender_id]
            # Create a NotificationEvent
            if room.type == RoomTypes.CHAT:
                event_type = EventTypes.MESSAGE
                if room.is_dm:
                    url = f"{url_for('chat_views.start_dm', user_id=sender_id)}"
                else:
                    url = f"{url_for('chat_views.global_chat')}"
                # print(f"[DEBUG NOTIFY ROOM] URL : {url}")
            elif room.type == RoomTypes.CIRCLE:
                if "Friend" in message_content:
                    url = f"{url_for('chat_views.friends_list')}"
                    event_type = EventTypes.FRIEND_REQUEST

                else:
                    url = f"{url_for('habit_views.habit_board')}"
                    event_type = EventTypes.REACTION
                room_name = request.current_user.username

            elif room.type == RoomTypes.COMMENT:
                event_type = EventTypes.COMMENT
                room_name = request.current_user.username
                url = f"{url_for('habit_views.single_habit_board',log_id='')}"
            else:
                event_type = EventTypes.POST
                if not room_name:
                    room_name = request.current_user.username

                url = f"{url_for('habit_views.habit_board')}"
            event = NotificationEvent(
                room_id=room_id,
                event_type=event_type,
                actor_id=sender_id,  # Set to sender's ID
                content=message_content,
                url=url
            )
            event.url = url
            session.add(event)
            session.commit()

            # # Log notification status for each user
            # for user_id in user_ids:
            #     notification_status = NotificationStatus(
            #         event_id=event.id, user_id=user_id, is_read=False)
            #     session.add(notification_status)

            session.commit()

            # Send push notifications
            for user_id in user_ids:
                NotificationService.send_push_notification_to_subs(
                    room_name, user_id, event)

    @staticmethod
    def send_push_notification_to_subs(room_name, recipient_id, event: NotificationEvent):
        """
        Send a push notification to the given user containing the message content
        and room information.

        :param recipient_id: The ID of the user to send the notification to
        :param room_name: The name of the room where the message was sent
        :param message_content: The content of the message
        :param url: The URL of the endpoint to navigate to when the notification is clicked
        """
        message_content, url = event.content, event.url
        with get_db_session() as session:

            user = session.query(User).filter_by(id=recipient_id).first()
            if not user or not user.push_subscription:
                # print(f"No push subscription found for user {recipient_id}")
                return

            payload = {
                "title": f"New {event.event_type.value} : {room_name}",
                "message": message_content,
                "url": url
            }
            # print("[DEBUG EVENT NOTIFICATION]User Subscription:",
                  user.push_subscription)
            try:
                webpush(
                    subscription_info = json.loads(user.push_subscription),
                    data = json.dumps(payload),
                    vapid_private_key = VAPID_PRIVATE_KEY,
                    vapid_claims = VAPID_CLAIMS
                )
                #print(f"Push notification sent to user {recipient_id}")

            except Exception as e:
                #print(f"WebPush failed for user {recipient_id}: {e}")

    @staticmethod
    def get_personal_room_id(user1_id, user2_id):
        import hashlib
        """
        Generate a unique room ID for two users by hashing a sorted combination of their IDs.
        """
        combined = '_'.join(sorted([str(user1_id), str(user2_id)]))
        return hashlib.md5(combined.encode()).hexdigest()

    @staticmethod
    def ensure_personal_room(user1_id, user2_id):
        """
        Check if a personal room exists for the two users.
        If not, create the room and add both subscribers.
        """
        with get_db_session() as session:
            room_id = NotificationService.get_personal_room_id(
                user1_id, user2_id)
            room = session.query(Room).filter_by(id=room_id).first()
            #print(f"[DEBUG EVENT PERSONAL] {room}")
            if not room:

                room = Room(
                    id=room_id,
                    type=RoomTypes.CIRCLE,  # Type circle used for personal notifications
                    name=f"Personal room for {user1_id} and {user2_id}"
                )
                session.add(room)
                session.commit()
                session.add(UserSubscription(
                    user_id=user1_id, room_id=room_id))
                session.add(UserSubscription(
                    user_id=user2_id, room_id=room_id))
                session.commit()
                #print(f"[DEBUG EVENT PERSONAL] {room}")

            return room

    @staticmethod
    def notify_personal_circle(sender_id, receiver_id, message_content):
        """
        Notify the receiver in their personal notification room, which is shared with the sender.
        """
        try:
            with get_db_session() as session:
                # Ensure the personal room exists (or create it if not)
                room = NotificationService.ensure_personal_room(
                    sender_id, receiver_id)
                if room:
                    NotificationService.notify_room(
                        room.id, sender_id, message_content)
                else:
                    #print(
                        f"Personal room not found for users {sender_id} and {receiver_id}")
                    logging.error(
                        f"Personal room not found for users {sender_id} and {receiver_id}")

        except Exception as e:
            logging.error(f"Error notifying personal circle: {e}")


@event_views.route("/notifications", methods=["GET"])
def get_notifications():
    """
    Retrieve and group notifications for the current user.

    Grouping logic:
    - COMMENT rooms: Group comment events by post (assuming the post ID is in NotificationEvent.content)
    - CIRCLE rooms: For rooms whose name starts with "circle_", count the number of new posts.
    - CHAT rooms: Ignore rooms named "Global". For DMs (rooms starting with "DM between"),
      extract the other user's name and count new chat messages.

    Only notifications with a null 'seen_at' are included.
    """
    current_user = request.current_user
    user_id = current_user.id
    notifications = []

    try:
        with get_db_session() as session:
            # Step 1: Find rooms where the user is subscribed
            user_rooms = session.query(Room).join(UserSubscription).filter(
                UserSubscription.user_id == user_id
            ).all()
            #print(f"[Debug Notifications rooms] {user_rooms}")
            comment_events_all = []
            # Process each room based on its type and naming convention
            for room in user_rooms:
                # Query unread notification events for the room via the NotificationStatus table
                events_query = session.query(NotificationEvent).filter(
                    NotificationEvent.room_id == room.id, NotificationEvent.actor_id != user_id).order_by(NotificationEvent.event_type)
                activity_status = session.query(ActivityStatus).filter_by(
                    room_id=room.id,
                    user_id=user_id
                ).first()

                last_seen = activity_status.updated_at if activity_status else None
                if room.type == RoomTypes.COMMENT:
                    comment_events = events_query.filter(
                        NotificationEvent.event_type == EventTypes.COMMENT,
                        NotificationEvent.created_at > last_seen if last_seen else True).order_by(NotificationEvent.created_at).all()
                    comment_events_all.append(comment_events)
                    ###
                    #print(f"[Debug Notifications COMMENT {comment_events}]")

                # CIRCLE rooms: if room name starts with "circle_", count new posts
                elif room.type == RoomTypes.CIRCLE:
                    if room.name.startswith("circle_"):
                        circle_events = events_query.filter(
                            NotificationEvent.event_type == EventTypes.POST,
                            NotificationEvent.created_at > last_seen if last_seen else True).all()
                        #print(f"[Debug Notifications CIRCLE {circle_events}]")
                        friend_id = room.name.split("_")[1]
                        friend = session.query(
                            User).get(friend_id)
                        count = len(circle_events)
                        if count > 0:
                            latest_time = max(
                                event.created_at for event in circle_events) if circle_events else None
                            notifications.append({
                                "room": room.name,
                                "room_type": "CIRCLE",
                                "url": f"{url_for('habit_views.habit_board')}",
                                "group": friend.id,
                                "count": count,
                                "latest_time": latest_time.isoformat() + 'Z',
                                "template": f"{count} new post{'s' if count != 1 else ''} from {friend.username}"
                            })
                    elif room.name.startswith("Personal"):
                        # this is a friend request list each room has one request
                        ids = room.name.split(" and ")
                        friend_id = ids[0].split(" for ")[1]
                        id2 = ids[1]
                        friend = session.query(User).get(friend_id)

                        request_events = events_query.filter(
                            NotificationEvent.event_type == EventTypes.FRIEND_REQUEST,
                            NotificationEvent.room_id == room.id
                        )

                        request_events = request_events.filter(
                            NotificationEvent.created_at > last_seen if last_seen else True).all()
                        count = len(request_events)

                        if count > 0:
                            latest_time = max(
                                event.created_at for event in request_events)
                            notifications.append({
                                "room": room.name,
                                "room_type": "PERSONAL",
                                "url": url_for('chat_views.friends_list'),
                                "group": friend.id,
                                "count": count,
                                "latest_time": latest_time.isoformat() + 'Z',
                                "template": f"{friend.username} sent you a friend request"
                            })

                # CHAT rooms: ignore global chat; handle DM rooms
                elif room.type == RoomTypes.CHAT:
                    # Ignore the Global chat room
                    if room.name.lower() == "global":
                        continue
                    # DM rooms expected to follow naming convention "DM between X and Y"
                    if room.name.startswith("DM between"):
                        chat_events = events_query.filter(
                            NotificationEvent.event_type == EventTypes.MESSAGE,
                            NotificationEvent.created_at > last_seen if last_seen else True).all()
                        #print(f"[Debug Notifications CHAT {chat_events}]")

                        count = len(chat_events)
                        if count > 0:
                            latest_time = max(
                                event.created_at for event in chat_events) if chat_events else None
                            # Extract the other user's name from the room name.
                            # Example: "DM between Alice and Bob" → if current_user is Alice, show Bob.
                            try:
                                parts = room.name.split("between")[
                                    1].strip().split("and")
                                if len(parts) == 2:
                                    user_a, user_b = parts[0].strip(
                                    ), parts[1].strip()
                                    other_user = user_b if user_a == current_user.username else user_a
                                    other_user_id = session.query(User).filter_by(
                                        username=other_user).first().id
                                else:
                                    other_user = "Unknown DM"
                            except Exception:
                                other_user = "Unknown DM"

                            notifications.append({
                                "room": room.name,
                                "room_type": "CHAT",
                                "url": f"{url_for('chat_views.start_dm', user_id=other_user_id)}",
                                "group": f"DM with {other_user}",
                                "count": count,
                                "latest_time": latest_time.isoformat() + 'Z',
                                "template": f"{other_user}: {count} new message{'s' if count != 1 else ''}"
                            })
                    else:
                        # For any other chat rooms, you may add additional grouping logic as needed
                        chat_events = events_query.filter(
                            NotificationEvent.event_type == None).all()
                        #print(f"[Debug Notifications None {chat_events}]")
                        count = len(chat_events)
                        if count > 0:
                            latest_time = max(
                                event.created_at for event in chat_events) if chat_events else None
                            notifications.append({
                                "room": room.name,
                                "room_type": "CHAT",
                                "group": room.name,
                                "count": count,
                                "latest_time": latest_time.isoformat() + 'Z',
                                "template": f"{room.name}: {count} new message{'s' if count != 1 else ''}"
                            })

            ###
            #print(f"[Debug Notifications COMMENT {comment_events_all}]")
            # Group events by post identifier extracted from content (this is an example logic)

            grouped = {}
            for event in comment_events_all:
                if not event:
                    continue
                event = event[0]
                event_room_id = event.room_id
                event_room_name = session.query(
                    Room).get(event_room_id).name
                post_id = event_room_name.split("_")[1]
                comment_origin = session.query(
                    Comment).get(post_id).entity_id
                post = session.query(Log).get(
                    comment_origin)
                if not post:
                    continue

                grouped.setdefault(
                    (post.habit_name, comment_origin), []).append(event)

            for post, events in grouped.items():
                count = len(events)
                latest_time = max(
                    event.created_at for event in events) if events else None
                notifications.append({
                    "room": events[0].room.name,
                    "room_type": "COMMENT",
                    "url": f"{events[0].url}{post[1]}?room={events[0].room.name}",
                    "group": f"Post {post[1]}",
                    "count": count,
                    "latest_time": latest_time.isoformat() + 'Z',
                    "template": f"{count} new comment{'s' if count != 1 else ''} on post {post[0]}"
                })
            notifications = sorted(
                notifications, key=lambda x: x["latest_time"] or "", reverse=True)

        return jsonify(notifications), 200

    except Exception as e:
        logging.error(f"Error fetching notifications: {e}")
        return jsonify({"error": "Failed to fetch notifications"}), 500
