#!/usr/bin/env python3
"""
Session_auth View Module
"""
from api.v2.views import app_views, auth_views
from flask import Blueprint
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

    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or len(email) == 0:
        return jsonify({'error': 'email missing'}), 400
    if password is None or len(password) == 0:
        return jsonify({'error': 'password missing'}), 400

    print(f"\n\n\npass: {password} \n\n\n")

    user = User.search({'email': email})
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

            response = jsonify(u.to_json())

            response.set_cookie(session_name, session_id,
                                max_age=auth.session_duration)
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
        return render_template('signup.html')

    email = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')

    # Validate input
    if not email:
        return jsonify({'error': 'email missing'}), 400
    if not password:
        return jsonify({'error': 'password missing'}), 400

    # Check if the email is already registered
    if User.search({'email': email}):
        return jsonify({'error': 'email already registered'}), 400

    try:
        # Create new user
        user = User(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        # Create a session for the new user
        session_id = auth.create_session(user.id)
        session_name = os.environ.get("SESSION_NAME", "_my_session_id")

        # Prepare the response with the session cookie
        response = jsonify(user.to_json())
        response.set_cookie(session_name, session_id,
                            max_age=auth.session_duration)
        if request.is_json:
            return response, 201
        else:
            # Redirect to dashboard.html and return HTML for a browser
            return render_template('dashboard.html', user=user)

    except Exception as e:
        return jsonify({'error': f'cannot create user: {str(e)}'}), 500

    return jsonify({})
