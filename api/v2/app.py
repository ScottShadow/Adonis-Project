#!/usr/bin/env python3
"""
Route module for the API
"""
from api.v2.auth.session_db_auth import SessionDBAuth
from os import getenv
from api.v2.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v2/*": {"origins": "*"}})
auth = None

auth = SessionDBAuth()


@app.before_request
def before_request() -> str:
    """
        This function is a before request hook that is executed before each
        request to the Flask application.

        :return: None
    """
    if auth is None:
        return
    forbidden_paths = [
        '/api/v2/status/',
        '/api/v2/unauthorized/', '/api/v2/forbidden/',
        "/api/v2/auth_session/login/"
    ]

    if auth.require_auth(request.path, forbidden_paths) is False:
        return  # type: ignore
    if auth.authorization_header(request) is None and \
            auth.session_cookie(request) is None:
        abort(401)
    if auth.current_user(request) is None:
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
