#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort
from api.v2.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v2/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v2/stats
    Return:
      - the number of each objects
    """
    from models.user import User
    from models.user_session import UserSession
    from models.log import Log
    from models.tag import Tag
    stats = {}
    stats['users'] = User.count()
    stats['user_sessions'] = UserSession.count()
    stats['logs'] = Log.count()
    stats['tags'] = Tag.count()

    return jsonify(stats)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """ GET /api/v2/unauthorized
    Return:
      - 401
    """
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden() -> str:
    """ GET /api/v2/forbidden
    Return:
      - 403
    """
    abort(403)


@app_views.route('/', strict_slashes=False)
def index() -> str:
    """ GET /
    Return:
      - 200
    """
    from flask import request, render_template
    if request.method == 'GET':
        return render_template('adonisLanding.html')
