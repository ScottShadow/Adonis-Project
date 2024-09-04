from functools import wraps
from flask import session, redirect, url_for, flash
import bcrypt


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You need to be logged in to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def hash_password(password: str) -> bytes:
    """
    Hashes a password using the bcrypt algorithm.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password as bytes.

    """
    PEPPER = "Adonis"  # Store as Master server system variable for security
    salt = bcrypt.gensalt(rounds=12)
    pepper_password = password + PEPPER
    return bcrypt.hashpw(pepper_password.encode("utf-8"), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check if a given password matches a hashed password.

    Args:
        hashed_password (bytes): The hashed password to compare against.
        password (str): The password to check.

    Returns:
        bool: True if the password matches the hashed password,
        False otherwise.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
