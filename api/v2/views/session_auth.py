#!/usr/bin/env python3
"""
Session_auth View Module
"""
from api.v2.views import app_views, auth_views
from flask import Blueprint, url_for, redirect
from authentication import hash_password, is_valid


@auth_views.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login() -> str:
    """ POST /api/v2/login
    Return:
      - 200
      - 400
    """
    # from api.v2.views import index
    from models.user import User
    from flask import request, jsonify, render_template
    from flask_babel import _

    if request.method == 'GET':
        return render_template('login.html')

    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
    else:
        # Handle form data for non-JSON requests (like from browsers)
        email = request.form.get('email')
        password = request.form.get('password')

    if email is None or len(email) == 0:
        return jsonify({'error': 'email missing'}), 400
    if password is None or len(password) == 0:
        return jsonify({'error': 'password missing'}), 400

    user = User.search_db({'email': email})
    if user is None or len(user) == 0:
        return jsonify({'error': 'no user found for this email'}), 404
    if not user[0].is_valid_password(password):
        return jsonify({'error': 'wrong password'}), 401

    try:
        from api.v2.app import auth
        from models.base import Base
        import os
        for u in user:
            session_id = auth.create_session(u.id)
            session_name = os.environ.get("SESSION_NAME", "_my_session_id")

            if request.is_json:
                response = jsonify(u.to_json())

                response.set_cookie(session_name, session_id,
                                    max_age=auth.session_duration, path='/', domain='127.0.0.1', samesite='Lax')
                return response, 201
            else:
                # Redirect to dashboard.html and return HTML for a browser
                response = redirect(url_for('app_views.dashboard_route'))
                response.set_cookie(session_name, session_id,
                                    max_age=auth.session_duration, path='/', domain='127.0.0.1', samesite='Lax')
                return response
    except Exception as e:
        return jsonify({'error': f'Cannot Login: {str(e)}'}), 500

    return jsonify({})


@auth_views.route('/logout', methods=['DELETE'],
                  strict_slashes=False)
def logout() -> str:
    """ DELETE /api/v2/logout
    Return:
      - 200
      - 403
    """
    # from api.v2.views import index
    from api.v2.app import auth
    from flask import request, jsonify

    if request:
        auth.destroy_session(request)
    return jsonify({})


@auth_views.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def signup() -> str:
    """ POST /api/v2/signup
    Return:
      - 201 on success with a session created and user logged in
      - 400 on failure
    """
    from models.user import User
    from flask import request, jsonify, render_template, redirect, url_for
    from flask_babel import _
    from api.v2.app import auth
    import os

    if request.method == 'GET':
        print("[DEBUG] GET request for signup")
        return render_template('signup.html')
    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
    else:
        # Handle form data for non-JSON requests (like from browsers)
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

    # Validate input
    if not email:
        print("[DEBUG] Email is missing")
        return jsonify({'error': 'email missing'}), 400
    if not password:
        print("[DEBUG] Password is missing")
        return jsonify({'error': 'password missing'}), 400

    # Check if the email is already registered
    # existing_users = User.search({'email': email})
    existing_users = User.search_db({'email': email})
    if existing_users:
        print(f"[DEBUG] Email already registered: {email}")
        return jsonify({'error': 'email already registered'}), 400

    try:
        print(f"[DEBUG] Creating new user with email: {email}")
        # Create new user
        user = User(
            email=email,
            username=username,
            password=hash_password(password),
            first_name=first_name,
            last_name=last_name
        )
        print(f"[DEBUG] Saving user to database: {user.to_json()}")
        user.save()

        # Create a session for the new user
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
            request = redirect(url_for('app_views.dashboard_route'))
            response.set_cookie(session_name, session_id,
                                max_age=auth.session_duration, path='/', domain='127.0.0.1', samesite='Lax')
            return response
            # Redirect to dashboard.html and return HTML for a browser

    except Exception as e:
        print(f"[DEBUG] Exception occurred: {str(e)}")
        return jsonify({'error': f'cannot create user: {str(e)}'}), 500

    return jsonify({})
