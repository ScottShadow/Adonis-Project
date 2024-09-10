#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v2")
auth_views = Blueprint("auth_views", __name__, url_prefix="/api/v2/auth_session")
log_views = Blueprint("log_views", __name__, url_prefix="/api/v2")
tag_views = Blueprint("tag_views", __name__, url_prefix="/api/v2")

from api.v2.views.index import *
from api.v2.views.users import *
from api.v2.views.session_auth import *
from api.v2.views.log_views import *

from models import *


User.load_from_file()
UserSession.load_from_file()
