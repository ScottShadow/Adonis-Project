#!/usr/bin/env python3
""" Module of Users views
"""
# from flask import Blueprint
from api.v2.views import app_views
from flask import abort, jsonify, request, redirect, url_for, render_template, Blueprint
from models.user import User
from authentication import hash_password
import os
from api.v2.app import auth


user_views = Blueprint("user_views", __name__, url_prefix="/api/v2")


@user_views.route('/profile', methods=['GET', 'POST'], strict_slashes=False)
def view_profile() -> str:
    """
    View and manage user profile.
    - GET: Renders user profile information.
    - POST: Updates user information via JSON or form data.
    """
    user = request.current_user
    if not user:
        abort(404)

    if request.method == 'GET':
        # Render the profile page if it's a GET request
        return render_template('user_profile.html', user=user)

    if request.method == 'POST':
        # Handle JSON or form data submission
        try:
            if request.is_json:
                # Handle JSON request
                data = request.get_json()
            else:
                # Handle form data submission
                data = request.form

            if not data.get('password'):
                return jsonify({'error': 'Password is required to update profile'}), 400
            # Validate the provided password
            if not user.is_valid_password(data.get('password')):
                return jsonify({'error': 'Invalid current password'}), 400
            # Update user attributes if provided
            if data.get('first_name'):
                user.first_name = data.get('first_name')
            if data.get('last_name'):
                user.last_name = data.get('last_name')
            if data.get('username'):
                user.username = data.get('username')
            if data.get('profile_info'):
                user.profile_info = data.get('profile_info')
            if data.get('new_password') and data.get('confirm_new_password'):
                new_password = data.get('new_password')
                confirm_new_password = data.get('confirm_new_password')
                if new_password != confirm_new_password:
                    return jsonify({'error': 'New password and confirmation do not match'}), 400
                user.password = hash_password(new_password)

            # Save the updated user information
            user.save()
            # Reset the session for the user
            auth.destroy_session(request)
            print(f"[DEBUG] Session ID Loading")
            session_id = auth.create_session(user.id)

            print(f"[DEBUG] Created session ID: {session_id}")
            session_name = os.environ.get("SESSION_NAME", "_my_session_id")

            if request.is_json:
                # Prepare the response with the session cookie
                response = jsonify(user.to_json())
                response.set_cookie(session_name, session_id,
                                    max_age=auth.session_duration, path='/', domain='127.0.0.1', samesite='Lax')
                print("[DEBUG] Returning JSON response")
                return response, 201
            else:
                print("[DEBUG] Redirecting to dashboard")
                response = redirect(url_for('user_views.view_profile'))
                response.set_cookie(session_name, session_id,
                                    max_age=auth.session_duration, path='/', domain='127.0.0.1', samesite='Lax')
                return response
                # Redirect to dashboard.html and return HTML for a browser
            # Return a JSON response for API clients

        except Exception as e:
            return jsonify({'error': f'Error updating profile: {str(e)}'}), 400


@user_views.route('/easter_egg', methods=['GET'], strict_slashes=False)
def easter_egg() -> str:
    """ GET /api/v2/easter_egg
    Renders the easter egg page.
    """
    return render_template('easter_egg.html')
