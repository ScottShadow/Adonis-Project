#!/usr/bin/env python3
"""
Main script to create a new user
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import User
from models.base import Base  # Import your base class

# Database setup
DATABASE_URL = "sqlite:///example.db"  # Update this to your actual database URL
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def create_user(email: str, username: str, password: str, first_name: str = None, last_name: str = None):
    """Create and add a new user to the database."""
    new_user = User(
        email=email,
        username=username,
        password=password,  # Password is set using the setter method
        first_name=first_name,
        last_name=last_name
    )

    # Add the user to the session and commit
    session.add(new_user)
    session.commit()

    print(f"User created: {new_user}")


if __name__ == "__main__":
    # Ensure that the tables are created
    Base.metadata.create_all(engine)

    # Example usage: create a new user
    create_user(
        email="john.doe@example.com",
        username="johndoe",
        password="securepassword123",
        first_name="John",
        last_name="Doe"
    )
