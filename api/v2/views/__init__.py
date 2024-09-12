#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v2")
auth_views = Blueprint("auth_views", __name__, url_prefix="/api/v2/")
log_views = Blueprint("log_views", __name__, url_prefix="/api/v2")
tag_views = Blueprint("tag_views", __name__, url_prefix="/api/v2")
user_views = Blueprint("user_views", __name__, url_prefix="/api/v2")
event_views = Blueprint('event_views', __name__, url_prefix="/api/v2")


from api.v2.views.index import *
from api.v2.views.app_views import *
from api.v2.views.session_auth import *
from api.v2.views.log_views import *
from api.v2.views.user_views import *
from api.v2.views.event_views import *

from models import *


User.load_from_file()
UserSession.load_from_file()
Log.load_from_file()
#Tag.load_from_file()
