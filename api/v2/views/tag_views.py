from models.tag import Tag
from models.user import User
from flask import jsonify, Blueprint

log_views = Blueprint('log_views', __name__, url_prefix="/api/v2")


@log_views.route('/user/<user_id>/tags', methods=['GET'])
def get_user_tags(user_id):
    """Retrieves tags for a given user"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        # Retrieve tags for the user
        tags = user.tags  # This assumes the relationship is set up correctly
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


@log_views.route('/tags', methods=['GET'])
def get_tags():
    """Retrieve all tags."""
    tags = Tag.query.all()
    tags_list = [{'id': tag.id, 'name': tag.name, 'description': tag.description, 'level': tag.level, 'category': tag.category} for tag in tags]
    return jsonify(tags_list)


@log_views.route('/tags/category/<category>', methods=['GET'])
def get_tags_by_category(category):
    """Retrieve tags by category."""
    tags = Tag.query.filter_by(category=category).all()
    tags_list = [{'id': tag.id, 'name': tag.name, 'description': tag.description, 'level': tag.level, 'category': tag.category} for tag in tags]
    return jsonify(tags_list)

if __name__ == '__main__':
    log_views.run(debug=True)