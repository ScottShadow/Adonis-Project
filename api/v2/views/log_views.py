#!/usr/bin/env python3
"""
Log View Module
"""
from api.v2.views import log_views
from flask import request, jsonify, render_template, Blueprint
from models.log import Log
from models.user import User
from api.v2.app import auth
from models.base import SessionLocal

log_views = Blueprint('log_views', __name__, url_prefix="/api/v2")


@log_views.route('/logs', methods=['GET'], strict_slashes=False)
def get_logs():
    """GET /api/v2/logs
    Retrieves all logs for the logged-in user, with optional filters.
    """
    session = None
    try:
        user = request.current_user
        if not user:
            return jsonify({'error': 'Unauthorized access'}), 401

        filters = {}
        habit_type = request.args.get('habit_type')
        if habit_type:
            filters['habit_type'] = habit_type

        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date and end_date:
            filters['date'] = (start_date, end_date)

        session = SessionLocal()
        logs_query = session.query(Log).filter_by(user_id=user.id, **filters)
        logs = logs_query.all()

        logs_json = [log.to_json() for log in logs]
        return jsonify(logs_json), 200

    except Exception as e:
        return jsonify({'error': f'Error retrieving logs: {str(e)}'}), 500
    finally:
        if session:
            session.close()


@log_views.route('/logs/create', methods=['POST'], strict_slashes=False)
def create_log():
    """POST /api/v2/logs
    Creates a new log for the logged-in user.
    """

    try:
        user = request.current_user
        if not user:
            print("[DEBUG CREATE LOG] Unauthorized access: No user found.")
            return jsonify({'error': 'Unauthorized access'}), 401

        if request.is_json:
            data = request.get_json()
            print(f"[DEBUG CREATE LOG] Received data: {data}")
            habit_type = data.get('habit_type')
            habit_name = data.get('habit_name')
            log_details = data.get('log_details', None)
        else:
            habit_type = request.form.get('habit_type')
            habit_name = request.form.get('habit_name')
            log_details = request.form.get('log_details', None)
        print(
            f"[DEBUG CREATE LOG] Parsed fields: habit_type={habit_type}, habit_name={habit_name}")

        # Debug the user and log information before saving
        print(f"[DEBUG CREATE LOG] Creating new log for user_id: {user.id}")

        new_log = Log(
            user_id=user.id,
            habit_type=habit_type,
            habit_name=habit_name,
            log_details=log_details,
        )
        print(
            f"[DEBUG CREATE LOG] Log Initialized successfully with id: {new_log.id}")

        new_log.save()

        print(
            f"[DEBUG CREATE LOG] Log saved successfully with id: {new_log.id}")

        return jsonify(new_log.to_json()), 201

    except Exception as e:
        print(f"[DEBUG CREATE LOG] Error occurred: {str(e)}")
        return jsonify({'error': f'Error creating log: {str(e)}'}), 500


@log_views.route('/logs/new', methods=['GET'], strict_slashes=False)
def new_log_form():
    """Serve the HTML form to create a new log"""
    return render_template('create_log.html')
