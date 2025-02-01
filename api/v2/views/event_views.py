from api.v2.views import log_views
from flask import request, jsonify, render_template, Blueprint, session as flask_session
from models.log import Log
from models.user import User
from api.v2.app import auth, logging
from models.models_helper import get_db_session
from flask import Flask, request, jsonify, Blueprint
from pywebpush import webpush, WebPushException
import json
import os
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
    payload = {
        "title": f"New message from {sender_name}",
        "message": message_content,
        "url": url
    }

    with get_db_session() as session:
        user = session.query(User).filter_by(id=recipient_id).first()
        if not user or not user.push_subscription:
            print(f"No push subscription found for user {recipient_id}")
            return

        try:
            webpush(
                subscription_info=json.loads(user.push_subscription),
                data=json.dumps(payload),
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS
            )
            print(f"Push notification sent to user {recipient_id}")

        except WebPushException as e:
            print("WebPush failed:", e)


@event_views.route("/send_notification", methods=["POST"])
def send_notification():
    data = request.json
    send_push_notification(data["title"], data["message"], data["url"])
    return jsonify({"message": "Notification sent!"}), 200


@event_views.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Notification sent!"}), 200


@event_views.route('/events/home', methods=['GET'], strict_slashes=False)
def home():
    return render_template('event_home.html')
