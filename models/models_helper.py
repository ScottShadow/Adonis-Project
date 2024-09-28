#!/usr/bin/env python3
from contextlib import contextmanager
from models.base import SessionLocal
"""
Model's Helper Module
"""


def calculate_xp(habit_type, difficulty="easy", custom_xp=None):
    """Calculate XP based on log details."""
    # Example XP calculation logic based on habit type
    xp_values = {
        'cardio': 15,
        'strength_training': 20,
        'stretching': 8,
        'yoga': 10,
        'meditation': 5,
        'reading': 7,
        'writing': 12,
        'coding': 25,
        'painting': 10,
        'music_practice': 12,
        'journaling': 6,
        'house_cleaning': 8,
        'gardening': 9,
        'meal_prep': 10,
        'sleep': 5,
    }
    # Difficulty multipliers
    difficulty_multiplier = {
        'trivial': 1,
        'easy': 2,
        'medium': 6,
        'hard': 24,
        'insane': 40,
    }
    if habit_type == 'custom':
        base_xp = custom_xp or 1  # Use user-specified XP for custom habits
    else:
        base_xp = xp_values.get(habit_type, 1)

    xp = base_xp * difficulty_multiplier.get(difficulty, 1)
    print(f"[DEBUG] XP for log : {xp}")

    return xp


@contextmanager
def get_db_session():
    session = None
    try:
        session = SessionLocal()
        yield session
    finally:
        if session:
            session.close()
