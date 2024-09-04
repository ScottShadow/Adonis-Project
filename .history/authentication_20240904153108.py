import bcrypt
import base64
from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You need to be logged in to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def hash_password(password: str) -> str:
    """
    Hashes a password using the bcrypt algorithm.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password as a base64 encoded string.
    """
    PEPPER = "Adonis"
    salt = bcrypt.gensalt(rounds=12)
    pepper_password = password + PEPPER
    hashed_bytes = bcrypt.hashpw(pepper_password.encode("utf-8"), salt)
    # Encode the hashed bytes to a base64 string
    return base64.b64encode(hashed_bytes).decode('utf-8')


def is_valid(stored_hashed_password: str, password: str) -> bool:
    """
    Check if a given password matches a hashed password.

    Args:
        stored_hashed_password (str): The base64 encoded hashed password.
        password (str): The password to check.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    PEPPER = "Adonis"
    peppered_password = password + PEPPER
    # Decode the base64 string back to bytes
    try:
        hashed_password_bytes = base64.b64decode(
            stored_hashed_password.encode('utf-8'))
    except Exception as e:
        print(f"Decoding error: {e}")
        return False
    return bcrypt.checkpw(peppered_password.encode("utf-8"), hashed_password_bytes)

# Test cases


def test_password_hashing_and_validation():
    password = "mysecretpassword"

    # Hash the password
    hashed_password = hash_password(password)
    print(f"Hashed Password: {hashed_password}")

    # Test validation
    is_valid_password = is_valid(hashed_password, password)
    print(f"Is the password valid? {is_valid_password}")

    # Test invalid password
    invalid_password = "wrongpassword"
    is_invalid_password = is_valid(hashed_password, invalid_password)
    print(f"Is the invalid password valid? {is_invalid_password}")


# Run the test
if __name__ == "__main__":
    test_password_hashing_and_validation()
