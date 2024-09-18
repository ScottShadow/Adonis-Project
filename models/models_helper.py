#!/usr/bin/env python3
from contextlib import contextmanager
from models.base import SessionLocal
"""
Model's Helper Module
"""


def calculate_xp(log):
    """Calculate XP based on log details."""
    # Example XP calculation logic based on habit type
    xp_values = {
        'exercise': 10,
        'meditation': 5,
        'reading': 7,
        'coding': 15
    }
    print(f"[DEBUG] XP for log : {xp_values.get(log.habit_type, 0)}")

    return xp_values.get(log.habit_type, 0)


@contextmanager
def get_db_session():
    session = None
    try:
        session = SessionLocal()
        yield session
    finally:
        if session:
            session.close()
