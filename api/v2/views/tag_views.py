from flask import jsonify, Blueprint
from sqlalchemy.orm import Session
from models.base import SessionLocal
from models.tag import Tag
from models.user import User

tag_views = Blueprint('tag_views', __name__, url_prefix="/api/v2")


@tag_views.route('/user/<user_id>/tags', methods=['GET'])
def get_user_tags(user_id):
    """Retrieves tags for a given user"""
    session = SessionLocal()
    try:
        user = session.query(User).get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        # Retrieve tags for the user
        tags = user.tags
        # Convert tags to a serializable format
        tags_data = [
            {
                "id": tag.id,
                "name": tag.name,
                "category": tag.category,
                "description": tag.description,
                "level": tag.level
            }
            for tag in tags
        ]
        return jsonify({"tags": tags_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@tag_views.route('/tags', methods=['GET'])
def get_tags():
    """Retrieve all tags."""
    session = SessionLocal()
    try:
        tags = session.query(Tag).all()
        tags_list = [
            {
                'id': tag.id,
                'name': tag.name,
                'description': tag.description,
                'level': tag.level,
                'category': tag.category
            }
            for tag in tags
        ]
        return jsonify(tags_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@tag_views.route('/tags/category/<category>', methods=['GET'])
def get_tags_by_category(category):
    """Retrieve tags by category."""
    session = SessionLocal()
    try:
        tags = session.query(Tag).filter_by(category=category).all()
        tags_list = [
            {
                'id': tag.id,
                'name': tag.name,
                'description': tag.description,
                'level': tag.level,
                'category': tag.category
            }
            for tag in tags
        ]
        return jsonify(tags_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


