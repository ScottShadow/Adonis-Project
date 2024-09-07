#!/usr/bin/env python3
"""
Route module for the API app.py
"""
from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v2.views import app_views, auth_views
from api.v2.auth.session_db_auth import SessionDBAuth
from db_setup import init_db
# from api.v2.views.users import users_views


app = Flask(__name__)
app.register_blueprint(app_views)
app.register_blueprint(auth_views)
# app.register_blueprint(users_views, url_prefix='/api/v2/users')
CORS(app, resources={r"/api/v2/*": {"origins": "*"}})
auth = None

auth = SessionDBAuth()
init_db()


@app.before_request
def before_request() -> str:
    """
        This function is a before request hook that is executed before each
        request to the Flask application.

        :return: None
    """
    print(f"\n\nRequest Path: {request.path}")
    print(f"\n\nRequest Endpoint: {request.endpoint}")
    if auth is None:
        return
    excluded_paths = [
        '/api/v2/status/', '/api/v2/stats',
        '/api/v2/unauthorized/', '/api/v2/forbidden/',
        "/api/v2/auth_session/login/", "/api/v2/auth_session/signup/"
    ]

    if auth.require_auth(request.path, excluded_paths) is False:
        return  # type: ignore
    if request.endpoint not in ['auth_views.signup', 'auth_views.login', 'app_views.create_user']:
        if auth.authorization_header(request) is None and \
                auth.session_cookie(request) is None:
            print("\n\nBefore Request abort 40 \n\n")
            abort(401)
    if request.endpoint not in ['app_views.create_user']:
        if auth.current_user(request) is None:
            print("BEFORE REQUEST FORBIDEN\n\n")
            abort(403)

    if auth.authorization_header(request) and auth.session_cookie(request):
        return None, abort(401)

    request.current_user = auth.current_user(request)


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
    app.run(host=host, port=port, debug=True)
