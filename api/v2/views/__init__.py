#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v2")
auth_views = Blueprint("auth_views", __name__, url_prefix="/api/v2/auth_session")

from api.v2.views.index import *
from api.v2.views.users import *
from api.v2.views.session_auth import *

User.load_from_file()
