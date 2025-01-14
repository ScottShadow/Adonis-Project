from api.v2.views import app_views
from flask import abort, jsonify, request, redirect, url_for, render_template, Blueprint, flash
from sqlalchemy.orm import joinedload, aliased
from sqlalchemy import func, and_
from models.room import Room
from models.message import Message
from models.user import User
from models.log import Log
from models.friendship import Friendship, FriendshipStatus
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
        # Get the total number of users excluding the current user
        total_users = session.query(User).filter(
            User.id != current_user_id).count()

        # Calculate pagination
        total_pages = ceil(total_users / per_page)

        # Fetch users for the current page
        users = (
            session.query(User.id, User.username)
            .filter(User.id != current_user_id)
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        # Fetch all relevant friendships for the current user
        friendships = session.query(Friendship).filter(
            (Friendship.user_id_1 == current_user_id) |
            (Friendship.user_id_2 == current_user_id)
        ).all()

        # Create a lookup dictionary for quick access
        friendships_lookup = {
            (f.user_id_1, f.user_id_2): f for f in friendships
        }

        # Create a dictionary to store the friendship statuses
        user_statuses = {}

        for user_id, username in users:
            # Determine friendship status using the lookup dictionary
            friendship = friendships_lookup.get(
                (current_user_id, user_id)
            ) or friendships_lookup.get(
                (user_id, current_user_id)
            )

            user_statuses[user_id] = {
                "username": username,
                "requester": (
                    "you" if friendship and friendship.user_id_1 == current_user_id
                    else "them" if friendship and friendship.user_id_2 == current_user_id
                    else None
                ),
                "status": friendship.status.value if friendship else None,
            }

        logging.debug("user_statuses: %s", user_statuses)

    return render_template(
        'people.html',
        friendship_statuses=user_statuses,
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


@chat_views.route('/friends/request/<user_id>', methods=['POST'])
def send_friend_request(user_id):
    """
    API endpoint to send a friend request to another user.
    :param user_id: The ID of the user to send a friend request to.
    :return: Response message with status code.
    """
    user = request.current_user  # Fetch current user
    if not user:
        logging.warning("Unauthorized access attempt.")
        abort(401, description="Unauthorized access.")

    current_user_id = user.id

    # Validate the target user ID
    with get_db_session() as session:
        other_user = session.query(User).filter_by(id=user_id).first()
        if not other_user:
            logging.warning(f"User with ID {user_id} not found.")
            abort(404, description="User not found.")

        # Check if a friendship already exists
        existing_friendship = session.query(Friendship).filter(
            ((Friendship.user_id_1 == current_user_id) & (Friendship.user_id_2 == user_id)) |
            ((Friendship.user_id_1 == user_id) &
             (Friendship.user_id_2 == current_user_id))
        ).first()

        if existing_friendship:
            if existing_friendship.status == FriendshipStatus.ACCEPTED:
                logging.info(
                    f"Friendship already exists between user {current_user_id} and {user_id}.")
                return "You are already friends.", 400
            elif existing_friendship.status == FriendshipStatus.REJECTED or existing_friendship.status == FriendshipStatus.PENDING:
                logging.info(
                    f"Friend request already sent from user {current_user_id} to {user_id}.")
                return "Friend request already sent.", 400

        # Create a new friendship with status 'pending'
        friendship = Friendship(
            user_id_1=current_user_id,
            user_id_2=user_id,
            status=FriendshipStatus.PENDING
        )
        logging.info(f"Friendship created: {friendship}")
        session.add(friendship)
        session.commit()

        logging.info(
            f"Friend request sent from user {current_user_id} to {user_id}.")

    return redirect(url_for('chat_views.people'))


@chat_views.route('/cancel_friend_request/<user_id>', methods=['POST'])
def cancel_friend_request(user_id):
    """Cancel a pending friend request."""
    user = request.current_user
    current_user_id = user.id

    with get_db_session() as session:
        # Find the friendship where the current user is the requester
        friendship = (
            session.query(Friendship)
            .filter(
                (Friendship.user_id_1 == current_user_id) & (Friendship.user_id_2 == user_id) &
                (Friendship.status == FriendshipStatus.PENDING)
            )
            .first()
        )

        if friendship:
            session.delete(friendship)
            session.commit()
            flash("Friend request canceled successfully.", "success")
        else:
            flash("No pending friend request found.", "error")

    return redirect(url_for('chat_views.people'))


@chat_views.route('/accept_friend_request/<user_id>', methods=['POST'])
def accept_friend_request(user_id):
    user = request.current_user
    current_user_id = user.id

    with get_db_session() as session:
        # Find the friendship request where the current user is the recipient (user_id_2)
        friendship = session.query(Friendship).filter(
            Friendship.user_id_1 == user_id,
            Friendship.user_id_2 == current_user_id,
            Friendship.status == FriendshipStatus.PENDING
        ).first()

        if friendship:
            # If a friendship request is found, update the status to "accepted"
            friendship.status = FriendshipStatus.ACCEPTED
            logging.info(
                f"Friendship accepted between user {current_user_id} and {user_id}.{friendship}"
            )
            session.commit()

            # Optionally, you can create a reverse friendship entry for user_id_2 to user_id_1 (bidirectional friendship)
            reverse_friendship = Friendship(
                user_id_1=current_user_id, user_id_2=user_id, status=FriendshipStatus.ACCEPTED)
            session.add(reverse_friendship)
            logging.info(
                f"Reverse friendship created between user {current_user_id} and {user_id}.{reverse_friendship}"
            )
            session.commit()

            flash('Friend request accepted!', 'success')
        else:
            flash('No pending friend request found.', 'danger')

    return redirect(url_for('chat_views.people'))


@chat_views.route('/reject_friend_request/<user_id>', methods=['POST'])
def reject_friend_request(user_id):
    user = request.current_user
    current_user_id = user.id

    with get_db_session() as session:
        # Find the pending friend request where the current user is the recipient
        friendship = session.query(Friendship).filter(
            Friendship.user_id_1 == user_id,
            Friendship.user_id_2 == current_user_id,
            Friendship.status == FriendshipStatus.PENDING
        ).first()

        if friendship:
            # Delete the friendship request
            session.delete(friendship)
            logging.info(
                f"Friendship request from user {user_id} to {current_user_id} rejected and removed.")
            session.commit()

            flash('Friend request rejected!', 'success')
        else:
            flash('No pending friend request found.', 'danger')

    return redirect(url_for('chat_views.people'))


@chat_views.route('/unfriend/<user_id>', methods=['POST'])
def unfriend(user_id):
    user = request.current_user
    current_user_id = user.id

    with get_db_session() as session:
        # Delete both directions of the friendship
        friendships = session.query(Friendship).filter(
            (Friendship.user_id_1 == current_user_id) & (Friendship.user_id_2 == user_id) |
            (Friendship.user_id_1 == user_id) & (
                Friendship.user_id_2 == current_user_id)
        ).all()

        if friendships:
            for friendship in friendships:
                session.delete(friendship)
            logging.info(
                f"Friendship between user {current_user_id} and {user_id} unfriended and removed.")
            session.commit()

            flash('Friend removed successfully!', 'success')
        else:
            flash('No friendship found to remove.', 'danger')

    return redirect(url_for('chat_views.people'))


@chat_views.route('/block_user/<user_id>', methods=['POST'])
def block_user(user_id):
    user = request.current_user
    current_user_id = user.id

    with get_db_session() as session:
        # Delete any existing friendship entries for these users
        session.query(Friendship).filter(
            (Friendship.user_id_1 == current_user_id) & (Friendship.user_id_2 == user_id) |
            (Friendship.user_id_1 == user_id) & (
                Friendship.user_id_2 == current_user_id)
        ).delete()

        # Create a new block entry where the blocker is user_id_1
        new_block = Friendship(
            user_id_1=current_user_id,
            user_id_2=user_id,
            status=FriendshipStatus.BLOCKED
        )
        session.add(new_block)
        logging.info(f"User {current_user_id} blocked user {user_id}.")
        session.commit()

    flash('User blocked successfully!', 'success')
    return redirect(url_for('chat_views.people'))


@chat_views.route('/unblock_user/<user_id>', methods=['POST'])
def unblock_user(user_id):
    user = request.current_user
    current_user_id = user.id

    with get_db_session() as session:
        # Locate the BLOCKED row where the current user is the blocker
        blocked_relationship = session.query(Friendship).filter(
            (Friendship.user_id_1 == current_user_id) &
            (Friendship.user_id_2 == user_id) &
            (Friendship.status == FriendshipStatus.BLOCKED)
        ).first()

        if blocked_relationship:
            # Remove the BLOCKED status by deleting the current relationship
            session.delete(blocked_relationship)

            # Recreate the symmetrical friendships with ACCEPTED status
            friendship_1 = Friendship(
                user_id_1=current_user_id,
                user_id_2=user_id,
                status=FriendshipStatus.ACCEPTED
            )
            friendship_2 = Friendship(
                user_id_1=user_id,
                user_id_2=current_user_id,
                status=FriendshipStatus.ACCEPTED
            )

            session.add_all([friendship_1, friendship_2])
            session.commit()

            logging.info(
                f"User {current_user_id} unblocked user {user_id} and restored friendships in both directions."
            )
            flash('User unblocked successfully and friendship restored!', 'success')
        else:
            flash('No block relationship found.', 'danger')

    return redirect(url_for('chat_views.people'))


@chat_views.route('/friends')
def friends_list():
    # Replace with your method of getting the logged-in user ID
    current_user_id = request.current_user.id

    with get_db_session() as session:

        # Step 1: Fetch friend IDs
        friend_ids_subquery = session.query(Friendship.user_id_2).filter(
            Friendship.user_id_1 == current_user_id,
            Friendship.status == FriendshipStatus.ACCEPTED
        ).subquery()

        logging.info(f"Friend IDs fetched for user {current_user_id}")
        logging.info(f"Friend IDs: {friend_ids_subquery}")

        # Step 2: Fetch user data, latest log timestamp, and habit_name
        friends_with_logs = session.query(
            User.id.label("friend_id"),
            User.username.label("friend_name"),
            User.level.label("friend_level"),
            func.max(Log.timestamp).label("last_log_date"),
            func.max(Log.habit_name).label("last_log_habit_name")
        ).outerjoin(Log, and_(Log.user_id == User.id, Log.visibility == "Public")).filter(
            User.id.in_(friend_ids_subquery)
        ).group_by(User.id).all()

        logging.info(f"Friends with logs fetched for user {current_user_id}")
        logging.info(f"Friends with logs: {friends_with_logs}")

    # Step 3: Format data for the frontend
    friends_dict = [
        {
            "id": friend.friend_id,
            "name": friend.friend_name,
            "level": friend.friend_level,
            "last_log_date": friend.last_log_date or "No public logs",
            "habit_name": friend.last_log_habit_name or "No recent habit"
        }
        for friend in friends_with_logs
    ]

    logging.info(f"Formatted friends data for user {current_user_id}")
    logging.info(f"Formatted friends data: {friends_dict}")

    # Step 4: Render the template
    return render_template("friend_page.html", friends=friends_dict)
