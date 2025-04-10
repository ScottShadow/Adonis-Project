#!/usr/bin/env python3
"""
Route module for the API app.py
"""
from api.v2.views.app_sockets import initialize_socketio, socketio
from populate_tags import seed_tags
from db_setup import init_db
from api.v2.auth.session_db_auth import SessionDBAuth
from api.v2.views import *
import logging
from os import getenv
from flask import Flask, jsonify, abort, request, redirect, url_for
from flask_cors import (CORS, cross_origin)
auth = None

logging.basicConfig(
    # Set the lowest level to capture (can adjust to INFO, WARNING, etc.)
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Logs to a file
        logging.StreamHandler()  # Logs to the console
    ]
)
# , auth_views, log_views, tag_views, user_views, event_views, chat_views, habit_views, interaction_views
# from api.v2.views.users import users_views


app = Flask(__name__)
app.config["SECRET_KEY"] = "adonis[the_first]@90314!"

app.register_blueprint(app_views)
app.register_blueprint(auth_views)
app.register_blueprint(log_views)
app.register_blueprint(tag_views)
app.register_blueprint(user_views)
app.register_blueprint(event_views)

app.register_blueprint(chat_views)
app.register_blueprint(habit_views)
app.register_blueprint(interaction_views)

CORS(app, resources={r"/api/v2/*": {"origins": "*"}},
     supports_credentials=True)
initialize_socketio(app)


auth = SessionDBAuth()
init_db()
# from models.base import init_migrate
# init_migrate(app)
# seed_tags()


@app.before_request
def before_request() -> str:
    """
    This function is a before request hook that is executed before each
    request to the Flask application.

    :return: None
    """
    # print(f"\n\n[DEBUG BEFORE REQUEST] Request Path: {request.path}")
    # print(f"[DEBUG BEFORE REQUEST] Request Endpoint: {request.endpoint}")

    # Check if the auth instance is set
    if auth is None:
        # print("[DEBUG BEFORE REQUEST] Auth is None, skipping authentication")
        return
    if request.path.startswith('/static'):
        return None
    # Define paths that don't require authentication
    excluded_paths = [
        '/api/v2/status/', '/api/v2/stats',
        '/api/v2/unauthorized/', '/api/v2/forbidden/',
        "/api/v2/login/", "/api/v2/signup/", "/api/v2/landing", "/wake_db"
    ]

    # Check if the current request path requires authentication
    if not auth.require_auth(request.path, excluded_paths):
        # print(f"[DEBUG BEFORE REQUEST] Path '{request.path}' does not require authentication")
        return  # No need for authentication, so continue the request

    # Check if the request endpoint is login or signup
    if request.endpoint not in ['auth_views.signup', 'auth_views.login', 'app_views.create_user']:
        # Check if there's no authorization header or session cookie
        if auth.authorization_header(request) is None and auth.session_cookie(request) is None:
            # print(f"[DEBUG BEFORE REQUEST] No authorization header or session cookie for '{request.endpoint}', aborting with 401")
            return redirect(url_for('auth_views.login'))

    # Check if the current user is authenticated
    if request.endpoint not in ['app_views.create_user']:
        if auth.current_user(request) is None:
            # print(f"[DEBUG BEFORE REQUEST] No current user for '{request.endpoint}', aborting with 403")
            return redirect(url_for('auth_views.login'))

    # Check for both authorization header and session cookie (which is unexpected)
    if auth.authorization_header(request) and auth.session_cookie(request):
        # print(f"[DEBUG BEFORE REQUEST] Both authorization header and session cookie found for '{request.endpoint}', aborting with 401")
        return redirect(url_for('auth_views.login'))

    # Set the current user for the request context
    request.current_user = auth.current_user(request)
    # print(f"[DEBUG BEFORE REQUEST] Current user set to: {request.current_user}")


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    socketio.run(app, debug=False, host=host,
                 allow_unsafe_werkzeug=True, port=5000)
