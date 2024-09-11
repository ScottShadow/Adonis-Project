from api.v2.views import log_views
from flask import request, jsonify, render_template, Blueprint
from models.log import Log
from models.user import User
from api.v2.app import auth
from models.base import SessionLocal

event_views = Blueprint('event_views', __name__, url_prefix="/api/v2")


@event_views.route('/events/home', methods=['GET'], strict_slashes=False)
def home():
    return render_template('event_home.html')
