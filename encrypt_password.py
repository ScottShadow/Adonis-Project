#!/usr/bin/env python3
"""
 Hashes a password using the bcrypt algorithm.
 Check if a given password matches a hashed password.
"""
import bcrypt


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
