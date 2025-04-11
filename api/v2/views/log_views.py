#!/usr/bin/env python3
"""
Log View Module
"""
from datetime import datetime
from api.v2.views import log_views
from flask import request, jsonify, render_template, Blueprint, url_for, redirect
from models.log import Log
from models.user import User
from models.base import SessionLocal
from models.models_helper import get_db_session
from sqlalchemy import func
from api.v2.app import logging

log_views = Blueprint('log_views', __name__, url_prefix="/api/v2")


def validate_date(date_str):
    """Validate if a string is in a valid date format."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


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

        filters = {'user_id': user.id}

        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        if data is None:
            return jsonify({'error': 'Invalid request data'}), 400
        habit_type = data.get('habit_type')
        if habit_type:
            filters['habit_type'] = habit_type

        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and not validate_date(start_date):
            return jsonify({'error': 'Invalid start_date format. Use YYYY-MM-DD.'}), 400
        if end_date and not validate_date(end_date):
            return jsonify({'error': 'Invalid end_date format. Use YYYY-MM-DD.'}), 400

        page = int(data.get('page', 1))
        limit = int(data.get('limit', 10))
        offset = (page - 1) * limit

        session = SessionLocal()

        # Base query
        logs_query = session.query(Log).filter_by(**filters)

        # Filter by dates if provided
        if start_date:
            # print(f"[DEBUG] Start date: {start_date}")
            logs_query = logs_query.filter(
                func.date(Log.created_at) >= start_date)
        if end_date:
            # print(f"[DEBUG] End date: {end_date}")
            logs_query = logs_query.filter(
                func.date(Log.created_at) <= end_date)

        # Pagination
        total_logs = logs_query.count()
        logs_query = logs_query.offset(offset).limit(limit)
        logs = logs_query.all()
        total_pages = (total_logs + limit - 1) // limit
        logs_json = [log.to_json() for log in logs]
        # Prepare the response with pagination metadata
        response = {
            'logs': logs_json,
            'pagination': {
                'current_page': page,
                'total_pages': total_pages,
                'total_logs': total_logs,
                'limit': limit
            }
        }
        return response, 200

    except Exception as e:
        return jsonify({'error': f'Error retrieving logs: {str(e)}'}), 500
    finally:
        if session:
            session.close()


@log_views.route('/logs/id/<string:log_id>', methods=['GET'], strict_slashes=False)
def get_log_with_id(log_id: str):
    """ GET /api/v2/logs/<log_id>
    Retrieves a single log by its str.
    """
    session = None
    try:
        session = SessionLocal()
        filters = {'id': log_id}
        log = session.query(Log).filter_by(**filters).first()
        # print(f"[DEBUG GET LOG] Retrieved log: {log}")
        if log:
            return jsonify(log.to_json()), 200
        else:
            return jsonify({'error': 'Log not get log with id found'}), 404
    except Exception as e:
        return jsonify({'error': f'Error retrieving log: {str(e)}'}), 500
    finally:
        if session:
            session.close()


@log_views.route('/logs/create', methods=['POST', 'GET'], strict_slashes=False)
def create_log():
    """POST /api/v2/logs
    Creates a new log for the logged-in user.
    """

    try:
        user = request.current_user
        if not user:
            logging.error(
                "[DEBUG CREATE LOG] Unauthorized access: No user found.")
            return jsonify({'error': 'Unauthorized access'}), 401

        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        # print(f"[DEBUG CREATE LOG] Received data: {data}")
        habit_type = data.get('habit_type')
        habit_name = data.get('habit_name')
        if not habit_type or not habit_name:
            return jsonify({
                'error': 'Both habit_type and habit_name are required to create a log.'
            }), 400

        log_details = data.get('log_details', None)
        # print(f"[DEBUG CREATE LOG] Parsed fields: habit_type={habit_type}, habit_name={habit_name}")

        # Debug the user and log information before saving
        # print(f"[DEBUG CREATE LOG] Creating new log for user_id: {user.id}")

        habit_type = request.form.get('habit_type')
        difficulty = request.form.get('difficulty')
        visibility = request.form.get('visibility')
        # print(f"[Debug CREATE LOG] Habit visibility: {visibility}")
        custom_xp = data.get('custom_xp')
        if len(custom_xp) == 0:
            custom_xp = 5
        from models.models_helper import calculate_xp
        xp_value = calculate_xp(habit_type=habit_type, difficulty=difficulty, custom_xp=int(
            custom_xp) if habit_type == 'custom' else None)
        logging.info(
            f"[DEBUG CREATE LOG] Calculated XP value: {xp_value} for habit type: {habit_type} and difficulty: {difficulty} and custom XP: {custom_xp}"
        )
        new_log = Log(
            user_id=user.id,
            habit_type=habit_type,
            habit_name=habit_name,
            log_details=log_details,
            visibility=visibility,
            xp=xp_value,
        )
        # Create log entry and calculate XP based on difficulty

        # print(f"[DEBUG CREATE LOG] Log Initialized successfully with id: {new_log.id} and XP {new_log.xp}")

        new_log.save()

        if new_log.visibility == 'Public':
            with get_db_session() as session:
                # Find the user's circle
                from models.room import Room, RoomTypes
                user_circle = session.query(Room).filter_by(
                    name=f"circle_{user.id}", type=RoomTypes.CIRCLE).first()

                if user_circle:
                    from api.v2.views.event_views import NotificationService
                    NotificationService.notify_room(
                        room_id=user_circle.id,
                        sender_id=user.id,
                        message_content=f"{user.username} added a new log: {new_log.habit_name}"
                    )
                    # print(f"[CREATE LOG] Notification sent to circle {user_circle.id}")
                    logging.info(
                        f"[CREATE LOG] Notification sent to circle {user_circle.id}")

        # print(f"[DEBUG CREATE LOG] Log saved successfully with id: {new_log.id}")
        if request.is_json:
            return jsonify(new_log.to_json()), 201
        else:
            response = redirect(url_for('app_views.dashboard_route'))
            return response

    except Exception as e:
        logging.error(f"[DEBUG CREATE LOG] Error occurred: {str(e)}")
        return jsonify({'error': f'Error creating log: {str(e)}'}), 500


@log_views.route('/logs/new', methods=['GET'], strict_slashes=False)
def new_log_form():
    """Serve the HTML form to create a new log"""
    return render_template('create_log.html')


@log_views.route('/logs/<log_id>', methods=['GET', 'POST'], strict_slashes=False)
def update_log(log_id):
    """PUT or PATCH /api/v2/logs/<log_id>
    Update a specific log for the logged-in user.
    """
    session = None

    try:
        user = request.current_user
        if not user:
            logging.warning(
                "Unauthorized access attempt for log_id: %s", log_id)
            return jsonify({'error': 'Unauthorized access'}), 401

        # Get the log to update
        with get_db_session() as session:
            logging.debug("Received log_id: %s", log_id)
            log = session.query(Log).filter_by(
                id=log_id, user_id=user.id).first()

            if not log:
                logging.error(
                    "Log not found for user_id: %s and log_id: %s", user.id, log_id)
                return jsonify({'error': 'Log not found'}), 404

            if request.method == 'GET':
                logging.info("Rendering update form for log_id: %s", log_id)
                return render_template('update_log.html', log=log)

            # Get the data to update
            if request.is_json:
                data = request.get_json()
                logging.debug("Received JSON data: %s", data)
            else:
                data = request.form
                logging.debug("Received form data: %s", data)

            if data is None:
                logging.error("Wrong format in request for log_id: %s", log_id)
                return jsonify({'error': 'Wrong format'}), 400

            # Update the fields if provided
            habit_type = data.get('habit_type')
            if habit_type:
                log.habit_type = habit_type
                logging.info("Updated habit_type for log_id: %s to %s",
                             log_id, habit_type)
            else:
                logging.warning(
                    "No habit_type provided for log_id: %s", log_id)
                return jsonify({'error': 'No habit_type provided'}), 400

            habit_name = data.get('habit_name')
            if habit_name:
                log.habit_name = habit_name
                logging.info("Updated habit_name for log_id: %s to %s",
                             log_id, habit_name)
            else:
                logging.warning(
                    "No habit_name provided for log_id: %s", log_id)
                return jsonify({'error': 'No habit_name provided'}), 400

            visibility = data.get('visibility')
            if visibility:
                log.visibility = visibility
                logging.info("Updated visibility for log_id: %s to %s",
                             log_id, visibility)
            else:
                logging.warning(
                    "No visibility provided for log_id: %s", log_id)
                return jsonify({'error': 'No visibility provided'}), 400

            log_details = data.get('log_details')
            log.log_details = log_details
            logging.info("Updated log_details for log_id: %s", log_id)

            # Update the `date_updated` field
            log.updated_at = datetime.utcnow()

            # Save the updated log
            session.add(log)
            session.commit()

        logging.info("Log successfully updated for log_id: %s", log_id)

        if request.is_json:
            return jsonify(log.to_json()), 200
        else:
            return redirect(url_for('app_views.dashboard_route'))

    except Exception as e:
        logging.error("Error updating log_id: %s - %s", log_id, str(e))
        return jsonify({'error': f'Error updating log: {str(e)}'}), 500


@log_views.route('/logs/delete/<log_id>', methods=['POST'], strict_slashes=False)
def delete_log(log_id):
    """DELETE /api/v2/logs/delete/<log_id>
    Deletes a specific log entry.
    """
    session = None
    try:
        user: User = request.current_user
        if not user:
            return jsonify({'error': 'Unauthorized access'}), 401

        session = SessionLocal()
        log = session.query(Log).filter_by(id=log_id, user_id=user.id).first()
        if not log:
            return jsonify({'error': 'Log not found'}), 404
        from models.models_helper import calculate_xp
        xp_to_deduct = log.xp_value
        logging.info("XP deducted: %s", xp_to_deduct)
        user.total_xp = user.total_xp - xp_to_deduct
        if user.total_xp < 0:
            user.total_xp = 0
        user.save()
        session.delete(log)
        session.commit()
        if request.is_json:
            return jsonify({'message': 'Log deleted successfully', 'new_xp': user.total_xp}), 200
        else:
            return redirect(url_for('app_views.dashboard_route'))

    except Exception as e:
        session.rollback()
        return jsonify({'error': f'Error deleting log: {str(e)}'}), 500
    finally:
        if session:
            session.close()

# obsolete


@log_views.route('/logs/update/<log_id>', methods=['GET', 'POST'], strict_slashes=False)
def update_log_form(log_id):
    """GET /api/v2/logs/<log_id>
    Renders the update form for a specific log and handles form submission for updates.
    """

    try:
        user = request.current_user
        if not user:
            return jsonify({'error': 'Unauthorized access'}), 401

        with get_db_session() as session:
            # print(f"[DEBUG UPDATE LOG] Received log_id: {log_id}")
            log = session.query(Log).filter_by(
                id=log_id, user_id=user.id).first()
            # print(f"[DEBUG] Request data: {request.args}, {request.form}")
            if not log:
                return jsonify({'error': 'Log not found'}), 404

            if request.method == 'POST':
                data = request.form if not request.is_json else request.get_json()

                # Update log attributes
                log.habit_type = data.get('habit_type', log.habit_type)
                log.habit_name = data.get('habit_name', log.habit_name)
                log.log_details = data.get('log_details', log.log_details)
                log.updated_at = datetime.utcnow()

                session.commit()

            if request.is_json:
                return jsonify(log.to_json()), 201
            else:
                response = redirect(url_for('app_views.dashboard_route'))
                return response

    except Exception as e:
        return jsonify({'error': f'Error updating log: {str(e)}'}), 500
