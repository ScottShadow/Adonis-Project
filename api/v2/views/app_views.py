#!/usr/bin/env python3
""" Module of Users views
"""
# from flask import Blueprint
from api.v2.views import app_views
from flask import abort, jsonify, request, redirect, url_for, render_template, jsonify
from models.user import User
from sqlalchemy import select
from models.models_helper import get_db_session
import os

# users_views = Blueprint("users_views", __name__)


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v2/users
    Return:
      - list of all User objects JSON represented
    """
    all_users = [user.to_json() for user in User.all_from_db()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """ GET /api/v2/users/:id
    Path parameter:
      - User ID
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    # user = User.get(user_id)
    user = request.current_user
    if user is None:
        abort(404)
    if user_id == "me" and request.current_user is None:
        abort(404)

    if user_id == "me" and request.current_user is not None:
        return jsonify(user.to_json())

    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """ DELETE /api/v2/users/:id
    Path parameter:
      - User ID
    Return:
      - empty JSON is the User has been correctly deleted
      - 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v2/users/
    JSON body:
      - email
      - password
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 400 if can't create the new User
    """
    rj = None
    error_msg = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None
    if rj is None:
        error_msg = "Wrong format"
    if error_msg is None and rj.get("email", "") == "":
        error_msg = "email missing"
    if error_msg is None and rj.get("password", "") == "":
        error_msg = "password missing"
    if error_msg is None:
        try:
            user = User(
                email=rj.get("email"),
                password=rj.get("password"),
                first_name=rj.get("first_name"),
                last_name=rj.get("last_name"),
                username=rj.get("username")
            )
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            error_msg = "Can't create User: {}".format(e)
    return jsonify({'error': error_msg}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """ PUT /api/v2/users/:id
    Path parameter:
      - User ID
    JSON body:
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
      - 400 if can't update the User
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    rj = None
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None
    if rj is None:
        return jsonify({'error': "Wrong format"}), 400
    if rj.get('first_name') is not None:
        user.first_name = rj.get('first_name')
    if rj.get('last_name') is not None:
        user.last_name = rj.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200


@app_views.route('/dashboard', methods=['GET'], strict_slashes=False)
def dashboard_route():
    """ GET /api/v2/dashboard
    Renders the dashboard page for the logged-in user.
    """
    try:
        # Ensure user is authenticated by checking session
        from api.v2.app import auth
        user = auth.current_user(request)
        if not user:
            return redirect(url_for('auth_views.login'))

        user_name = user.username
        current_xp = user.total_xp
        user_level = user.level

        xp_needed_current = xp_for_current_level(user_level)
        xp_needed_next = xp_for_next_level(user_level)

        xp_progress = current_xp - xp_needed_current
        xp_percentage = (xp_progress / (xp_needed_next - xp_needed_current)
                         ) * 100 if xp_needed_next > xp_needed_current else 0
        print(f"user.total_xp: {user.total_xp} (type: {type(user.total_xp)})")
        print(f"user.level: {user.level} (type: {type(user.level)})")

        # Fetch recent logs
        recent_logs = user.logs  # Assuming logs is ordered by date
        print(f"recent_logs: {recent_logs} (type: {type(recent_logs)})")
        if request.is_json:
            return jsonify({})
        else:
            print("Rendering user_dashboard.html")
            return render_template('user_dashboard.html',
                                   user_name=user_name,
                                   user_level=user_level,
                                   current_xp=current_xp,
                                   xp_needed=xp_needed_next,
                                   xp_percentage=xp_percentage,
                                   recent_logs=recent_logs,
                                   VAPID_PUBLIC_KEY=os.environ.get(
                                       'VAPID_PUBLIC_KEY'),
                                   MY_WEBSITE_URL=os.environ.get('MY_WEBSITE_URL', "http://localhost:5000/"))

    except Exception as e:
        return jsonify({'error': f'Error loading dashboard: {str(e)}'}), 500


def xp_for_next_level(user_level):
    """ Calculates how much XP is needed for the next level """
    from api.v2.app import logging

    if user_level == 0:
        return 100
    res = ((user_level+1) ** 2) * 100
    logging.debug("user_level == %s -- res-next == %s, ", user_level, res)

    return res


def xp_for_current_level(user_level):
    """ Returns the XP required for the current level"""
    from api.v2.app import logging
    if user_level == 0:
        return 0
    res = ((user_level) ** 2) * 100
    logging.debug("user_level == %s -- res-curent == %s, ", user_level, res)

    return res


@app_views.route('/sw.js', methods=['GET'], strict_slashes=False)
def service_worker():
    import os
    from flask import current_app, send_from_directory, make_response
    # Print the current app root for debugging
    print(f"current_app.root_path: {current_app.root_path}")

    # Adjust the path relative to current_app.root_path (which is in api/v2/views)
    sw_path = os.path.join(current_app.root_path, 'static', 'scripts')
    sw_path = os.path.abspath(sw_path)  # Get the absolute path

    print(f"Serving sw.js from: {sw_path}")  # Debug: Verify the path

    response = make_response(send_from_directory(sw_path, 'sw.js'))
    # Allow the service worker to control pages from the root
    response.headers['Service-Worker-Allowed'] = '/'
    return response


@app_views.route("/wake_db", methods=['GET'], strict_slashes=False)
def wake_db():
    with get_db_session() as session:
        session.query(User).filter_by(id=1).first()
    return jsonify({"message": "Database is awake"}), 200
