from flask import Blueprint, request, jsonify
from sqlalchemy import func
from sqlalchemy.orm import Session
from models.interaction import Reaction, EntityType, ReactionType, Comment
from models.models_helper import get_db_session
from .event_views import NotificationService
interaction_views = Blueprint(
    "interaction_views", __name__, url_prefix="/api/v2")


@interaction_views.route("/reactions", methods=["POST"])
def add_reaction():
    """Add a reaction to an entity."""
    data = request.json
    user_id = request.current_user.id
    post_owner_id = data.get("user_id").strip()
    entity_id = data.get("entity_id")
    entity_type = EntityType(data.get("entity_type"))
    reaction_type = ReactionType(data.get("reaction_type"))

    if not all([post_owner_id, entity_id, entity_type, reaction_type]):
        return jsonify({"error": "Missing required fields"}), 400

    with get_db_session() as session:
        # Prevent duplicate reactions
        existing = session.query(Reaction).filter_by(
            user_id=user_id, entity_id=entity_id, entity_type=entity_type, reaction_type=reaction_type
        ).first()

        if existing:
            session.delete(existing)
            session.commit()
            return jsonify({"message": "User already reacted reaction removed"}), 204

        new_reaction = Reaction(
            user_id=user_id,
            entity_id=entity_id,
            entity_type=entity_type,
            reaction_type=reaction_type,
        )
        session.add(new_reaction)
        session.commit()
        from .event_views import NotificationService
        from models.user import User
        sender = session.query(User.username).filter_by(id=user_id).first()[0]
        notification_content = f"You {reaction_type.value} {sender}"
        NotificationService.notify_personal_circle(
            user_id, post_owner_id, notification_content)

    return jsonify({"message": "Reaction added successfully"}), 201


@interaction_views.route("/reactions/<reaction_id>", methods=["DELETE"])
def remove_reaction(reaction_id):
    """Remove a user's reaction from an entity."""
    with get_db_session() as session:
        reaction = session.query(Reaction).filter_by(id=reaction_id,).first()
        if not reaction:
            return jsonify({"error": "Reaction not found"}), 404

        session.delete(reaction)
        session.commit()

    return jsonify({"message": "Reaction removed successfully"}), 200


@interaction_views.route("/reactions/counts/<entity_id>/<entity_type>", methods=["GET"])
def get_all_reaction_counts(entity_id, entity_type):
    """Get aggregated reaction counts for an entity."""
    with get_db_session() as session:
        counting = (
            session.query(Reaction.reaction_type, func.count(Reaction.id))
            .filter(Reaction.entity_id == entity_id, Reaction.entity_type == entity_type)
            .group_by(Reaction.reaction_type)
            .all()
        )

    counts = {reaction: count for reaction, count in counting}
    return jsonify({
        "entity_id": entity_id,
        "entity_type": entity_type,
        "reactions": counts
    })


@interaction_views.route("/reactions/all/<entity_id>/<entity_type>", methods=["GET"])
def get_all_reactions(entity_id, entity_type):
    """Fetch all reactions for an entity (for UI)."""
    with get_db_session() as session:
        reactions = session.query(Reaction).filter_by(
            entity_id=entity_id, entity_type=entity_type).all()
    return jsonify([{"user_id": r.user_id, "reaction_type": r.reaction_type} for r in reactions])


@interaction_views.route("/comments", methods=["POST"])
def create_comment():
    """Create a new comment on a post, habit_log, or event."""
    current_user = request.current_user
    data = request.get_json()
    required_fields = ["user_id", "entity_id", "entity_type", "text"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    try:
        data["entity_type"] = EntityType(
            data["entity_type"])  # Convert string to Enum
    except ValueError:
        return jsonify({"error": "Invalid entity_type"}), 400
    with get_db_session() as session:
        comment = Comment(user_id=current_user.id, entity_id=data["entity_id"],
                          entity_type=data["entity_type"], text=data["text"])
        session.add(comment)
        from models.room import Room, RoomTypes, UserSubscription
        comment_room = session.query(Room).filter_by(
            name=f"comment_{comment.id}").first()
        if not comment_room:
            comment_room = Room(
                name=f"comment_{comment.id}", is_dm=False, type=RoomTypes.COMMENT)
            session.add(comment_room)

            subscription = UserSubscription(
                user_id=current_user.id,
                room_id=comment_room.id,
            )
            session.add(subscription)
            if not data["user_id"] == current_user.id:
                subscription2 = UserSubscription(
                    user_id=data["user_id"],
                    room_id=comment_room.id,
                )

                session.add(subscription2)
            session.commit()
        NotificationService.notify_room(
            comment_room.id, current_user.id, comment.text)

        return jsonify({"message": "Comment added", "comment_id": comment.id}), 201


@interaction_views.route("/comments/<entity_id>/<entity_type>", methods=["GET"])
def get_comments(entity_id, entity_type):
    """Retrieve all comments for a given entity."""
    with get_db_session() as session:
        comments = session.query(Comment).filter_by(
            entity_id=entity_id, entity_type=entity_type).all()
        return jsonify([{"id": c.id, "user_id": c.user_id, "text": c.text, "created_at": c.created_at} for c in comments]), 200


@interaction_views.route("/comments/<comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    """Delete a comment if the user owns it."""
    with get_db_session() as session:
        comment = session.query(Comment).filter_by(id=comment_id).first()
        if not comment:
            return jsonify({"error": "Comment not found"}), 404
        session.delete(comment)
        session.commit()
        return jsonify({"message": "Comment deleted"}), 203
