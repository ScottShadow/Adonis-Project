#!/usr/bin/env python3
"""
Log View Module
"""
from datetime import datetime
from api.v2.views import log_views
from flask import request, jsonify, render_template, Blueprint, url_for, redirect
from models.log import Log
from models.user import User
from api.v2.app import auth
from models.base import SessionLocal
from sqlalchemy import func

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
            data = request.form()
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
            print(f"[DEBUG] Start date: {start_date}")
            logs_query = logs_query.filter(
                func.date(Log.created_at) >= start_date)
        if end_date:
            print(f"[DEBUG] End date: {end_date}")
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


@log_views.route('/logs/<string:log_id>', methods=['GET'], strict_slashes=False)
def get_log_with_id(log_id: str):
    """ GET /api/v2/logs/<log_id>
    Retrieves a single log by its str.
    """
    session = None
    try:
        session = SessionLocal()
        filters = {'id': log_id}
        log = session.query(Log).filter_by(**filters).first()
        print(f"[DEBUG GET LOG] Retrieved log: {log}")
        if log:
            return jsonify(log.to_json()), 200
        else:
            return jsonify({'error': 'Log not get log with id found'}), 404
    except Exception as e:
        return jsonify({'error': f'Error retrieving log: {str(e)}'}), 500
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
        else:
            data = request.form

        print(f"[DEBUG CREATE LOG] Received data: {data}")
        habit_type = data.get('habit_type')
        habit_name = data.get('habit_name')
        if not habit_type or not habit_name:
            return jsonify({
                'error': 'Both habit_type and habit_name are required to create a log.'
            }), 400

        log_details = data.get('log_details', None)
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


@log_views.route('/logs/<string:log_id>', methods=['PUT', 'PATCH'], strict_slashes=False)
def update_log(log_id: str):
    """PUT or PATCH /api/v2/logs/<log_id>
    Update a specific log for the logged-in user.
    """
    session = None

    try:
        user = request.current_user
        if not user:
            return jsonify({'error': 'Unauthorized access'}), 401

        # Get the log to update
        session = SessionLocal()
        print(f"[DEBUG UPDATE LOG] Received log_id: {log_id}")
        log = session.query(Log).filter_by(id=log_id, user_id=user.id).first()

        if not log:
            return jsonify({'error': 'Log not found or unauthorized'}), 404

        # Get the data to update
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        # Update the fields if provided
        habit_type = data.get('habit_type')
        if habit_type:
            log.habit_type = habit_type

        habit_name = data.get('habit_name')
        if habit_name:
            log.habit_name = habit_name

        log_details = data.get('log_details')
        if log_details:
            log.log_details = log_details

        # Update the `date_updated` field
        log.updated_at = datetime.utcnow()

        # Save the updated log
        session.add(log)
        session.commit()

        if request.is_json:
            return jsonify(log.to_json()), 200
        else:
            return redirect(url_for('app_views.dashboard_route', log_id=log_id))

    except Exception as e:
        return jsonify({'error': f'Error updating log: {str(e)}'}), 500
    finally:
        if session:
            session.close()


@log_views.route('/logs/delete/<string:log_id>', methods=['DELETE'], strict_slashes=False)
def delete_log(log_id):
    """DELETE /api/v2/logs/delete/<log_id>
    Deletes a specific log entry.
    """
    session = None
    try:
        user = request.current_user
        if not user:
            return jsonify({'error': 'Unauthorized access'}), 401

        session = SessionLocal()
        log = session.query(Log).filter_by(id=log_id, user_id=user.id).first()
        if not log:
            return jsonify({'error': 'Log not found'}), 404

        session.delete(log)
        session.commit()
        return jsonify({'message': 'Log deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': f'Error deleting log: {str(e)}'}), 500
    finally:
        if session:
            session.close()


@log_views.route('/logs/<string:log_id>', methods=['GET', 'POST'], strict_slashes=False)
def update_log_form(log_id: str):
    """GET /api/v2/logs/<log_id>
    Renders the update form for a specific log and handles form submission for updates.
    """
    session = None

    try:
        user = request.current_user
        if not user:
            return jsonify({'error': 'Unauthorized access'}), 401

        session = SessionLocal()
        print(f"[DEBUG UPDATE LOG] Received log_id: {log_id}")
        log = session.query(Log).filter_by(id=log_id, user_id=user.id).first()
        print(
            f"[DEBUG] Request data: {request.args}, {request.form}")
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

            return redirect(url_for('app_views.dashboard_route'))

        # Render the form with existing log details
        return render_template('update_log.html', log=log_id)

    except Exception as e:
        return jsonify({'error': f'Error updating log: {str(e)}'}), 500
    finally:
        if session:
            session.close()
