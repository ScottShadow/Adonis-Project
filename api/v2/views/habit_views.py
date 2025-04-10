#!/usr/bin/env python3
"""
Habit View Module
"""
from datetime import datetime
from api.v2.views import log_views
from flask import request, jsonify, render_template, Blueprint, url_for, redirect
from models.log import Log
from models.user import User
from models.friendship import Friendship, FriendshipStatus
from models.interaction import Comment, Reaction, EntityType, ReactionType
from api.v2.app import auth
from models.base import SessionLocal
from models.models_helper import get_db_session
from sqlalchemy import func
from api.v2.app import logging

habit_views = Blueprint('habit_views', __name__, url_prefix="/api/v2")


def organize_habit_board_feed(logs):
    habit_feed = []
    # Fetch reactions and comments for all logs
    with get_db_session() as session:
        for log in logs:
            reactions = session.query(
                Reaction.reaction_type,
                func.count(Reaction.id).label("count")
            ).filter_by(entity_id=log["log_id"]).group_by(Reaction.reaction_type).all()
            comments = session.query(Comment).filter_by(
                entity_id=log["log_id"]).all()  # Function to fetch comments

            formatted_log = {
                "id": log["log_id"],
                # Adjust based on your User model
                "user": {"username": log["user"]["username"], "owner_id": log["user"]["id"]},
                "habit_type": log["habit_type"],
                "habit_name": log["habit_name"],
                "log_details": log["log_details"],
                "timestamp": log["timestamp"].isoformat() + 'Z',
                "streak": log.get("streak", 0),
                "xp": log.get("xp", 0),
                "reactions": {reaction_type.value: count for reaction_type, count in reactions},
                "comments": [{"user": {"username": c.user.username, "user_id": c.user.id}, "text": c.text, "id": c.id} for c in comments]
            }
            habit_feed.append(formatted_log)
    return habit_feed


@habit_views.route('/habit_board', methods=['GET'], strict_slashes=False)
def habit_board():
    print(f"[DEBUG] Rendering habit_board.html")

    user = request.current_user
    logs, rooms = get_habit_board_feed(user.id)
    habit_feed: list = organize_habit_board_feed(logs)
    # print(f"[DEBUG] Habit Feed: {habit_feed}")
    current_user = {"id": user.id, "username": user.username}
    return render_template('habit_board.html', logs=habit_feed, current_user=current_user, rooms=list(rooms))


@habit_views.route('/habit_board/<log_id>', methods=['GET'], strict_slashes=False)
def single_habit_board(log_id):
    print(f"[DEBUG] Fetching Habit Log ID: {log_id}")

    user = request.current_user
    room = request.args.get("room")

    current_user = {"id": user.id, "username": user.username}

    with get_db_session() as session:
        # verify if user exist in room
        from models import Room, Comment
        this_room = session.query(Room).filter(Room.name == room).first()
        exists = current_user.get("id") in this_room.users
        log = session.query(
            Log.id,
            Log.habit_name,
            Log.habit_type,
            Log.log_details,
            Log.created_at.label("timestamp"),
            User.id.label("user_id"),
            User.username.label("user_name")
        ).join(User, Log.user_id == User.id).filter(
            Log.id == log_id,
            Log.visibility == "Public"
        ).first()

        if not log or not room or not exists:
            return "Log not found or unauthorized", 404

        if "comment" in room:
            # Get all comment rooms where entity_id matches log_id
            all_comment_ids = session.query(Comment.id).filter(
                Comment.entity_id == log_id).all()
            all_comment_ids = [comment_id for (comment_id,) in all_comment_ids]
            all_comment_rooms = [
                f"comment_{comment_id}" for comment_id in all_comment_ids]
            rooms = session.query(Room.id).filter(
                Room.name.in_(all_comment_rooms)).all()
            rooms = [rooms[0] for rooms in rooms]
        room_id = session.query(Room.id).filter_by(name=room).first()[0]
        log = [
            {
                "log_id": log.id,
                "habit_name": log.habit_name,
                "habit_type": log.habit_type,
                "log_details": log.log_details,
                "timestamp": log.timestamp,
                "user": {
                    "id": log.user_id,
                    "username": log.user_name,
                    # "avatar": log.user_avatar,
                }
            }
            for log in [log]
        ]
        processed_log = organize_habit_board_feed(log)

    return render_template(
        'habit_board.html',
        logs=processed_log,
        current_user=current_user,
        rooms=rooms
    )


@habit_views.route('/habit_board/comments', methods=['GET'], strict_slashes=False)
def habit_board_comments():
    print(f"[DEBUG] getting alpine comments")
    user = request.current_user
    logs, _ = get_habit_board_feed(user.id)
    habit_feed = organize_habit_board_feed(logs)
    comments = [comment for c in habit_feed for comment in c['comments']]
    return jsonify(comments)


def get_habit_board_feed(user_id, limit=50, order_by="latest"):
    with get_db_session() as session:
        from models.room import Room, UserSubscription, RoomTypes
        from models.user import User
        from models.log import Log

        # Step 1: Find rooms where the user is subscribed
        user_rooms = session.query(Room).join(UserSubscription).filter(
            UserSubscription.user_id == user_id
        ).all()

        # Step 2: Filter the rooms to only circles
        circle_rooms = [
            room for room in user_rooms if room.type == RoomTypes.CIRCLE]
        circle_rooms_ids = [rooms.id for rooms in circle_rooms]
        # Step 3: Extract owner IDs from circle names (format: "circle_ownerid")
        owner_ids = set()
        for room in circle_rooms:
            if room.name.startswith("circle_"):
                # Expecting name like "circle_12345", so split and take the owner id
                parts = room.name.split("circle_")
                if len(parts) > 1 and parts[1]:
                    owner_ids.add(parts[1])

        # Optionally, include the current user in the feed
        owner_ids.add(user_id)

        # Step 4: Query logs from these owner IDs
        query = session.query(
            Log.id,
            Log.habit_name,
            Log.habit_type,
            Log.log_details,
            Log.created_at.label("timestamp"),
            User.id.label("user_id"),
            User.username.label("user_name")
        ).join(User, Log.user_id == User.id).filter(
            Log.user_id.in_(list(owner_ids)),
            Log.visibility == "Public"
        )

        # Order results (if needed)
        if order_by == "latest":
            query = query.order_by(Log.created_at.desc())

        # Return structured logs
        return [
            {
                "log_id": log.id,
                "habit_name": log.habit_name,
                "habit_type": log.habit_type,
                "log_details": log.log_details,
                "timestamp": log.timestamp,
                "user": {
                    "id": log.user_id,
                    "username": log.user_name,
                    # "avatar": log.user_avatar,
                }
            }
            for log in query.limit(limit).all()
        ], circle_rooms_ids
