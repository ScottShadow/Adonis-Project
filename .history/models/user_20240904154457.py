#!/usr/bin/env python3
"""Combined User Model Module"""
from datetime import datetime

import hashlib
from models.base import Base as SQLAlchemyBase, BaseClass
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, func
from sqlalchemy.orm import relationship, backref
from typing import TYPE_CHECKING
from models import user_tags

# Many-to-Many relationship table for users and tags

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
if TYPE_CHECKING:
    from models.log import Log

# from models.friendship import Friendship


class User(BaseClass, SQLAlchemyBase):
    """Combined User class using SQLAlchemy and custom methods"""
    __tablename__ = "users"

    id = Column(String, primary_key=True, nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    username = Column(String(250), nullable=False,
                      unique=True)  # User's chosen name
    hashed_password = Column("hashed_password", String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
    first_name = Column(String(250), nullable=True)
    last_name = Column(String(250), nullable=True)
    # Assumes skills are stored as a comma-separated string
    skills = Column(String, nullable=True)

    # Additional profile details like bio, profile picture URL
    profile_info = Column(String(500), nullable=True)
    total_xp = Column(Integer, default=0)  # Aggregate XP earned through logs
    # When the account was created
    account_created_at = Column(DateTime, default=func.now())
    last_login = Column(DateTime, nullable=True)  # Last login timestamp

    # Relationships
    logs = relationship('Log', back_populates='user')
    """ friendships_1 = relationship(
        'Friendship', foreign_keys='Friendship.user_id_1', back_populates='user_1')
    friendships_2 = relationship(
        'Friendship', foreign_keys='Friendship.user_id_2', back_populates='user_2')

    friends = relationship(
        'User',
        secondary='friendships',
        primaryjoin=id == Friendship.user_id_1,
        secondaryjoin=id == Friendship.user_id_2,
        backref=backref('user_friends', lazy='dynamic'),
        overlaps='friendships_1,friendships_2',
    ) """
    tags = relationship('Tag', secondary='user_tags', back_populates='users')

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a User instance"""
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        if not self.email:
            raise ValueError("Email is required for User creation")

        self.username = kwargs.get('username')
        if not self.username:
            raise ValueError("Username is required for User creation")

        # Password is passed as a plain text and will be hashed in the setter
        password = kwargs.get('password', kwargs.get('_hashed_password'))
        if not password:
            raise ValueError("Password is required for User creation")
        self.password = password  # Will be hashed by the setter method

        # Optional, default to empty string
        self.first_name = kwargs.get('first_name', "")
        # Optional, default to empty string
        self.last_name = kwargs.get('last_name', "")
        self.session_id = kwargs.get(
            'session_id', None)  # Optional, can be None
        self.reset_token = kwargs.get(
            'reset_token', None)  # Optional, can be None
        self.skills = kwargs.get('skills', None)  # Optional, can be None
        self.profile_info = kwargs.get(
            'profile_info', None)  # Optional, can be None
        self.total_xp = kwargs.get('total_xp', 0)  # Optional, default to 0
        self.last_login = kwargs.get(
            'last_login', None)  # Optional, can be None

    @ property
    def password(self) -> str:
        """Getter for the hashed password"""
        return self._hashed_password

    @ password.setter
    def password(self, pwd: str):
        """Setter for a new password: encrypt using SHA256"""
        if pwd is None or not isinstance(pwd, str):
            self._hashed_password = None
        else:
            self._hashed_password = hashlib.sha256(
                pwd.encode()).hexdigest().lower()

    def is_valid_password(self, pwd: str) -> bool:
        """Check if the given password matches the stored hashed password"""
        if pwd is None or not isinstance(pwd, str):
            return False
        if self.password is None:
            return False
        return hashlib.sha256(pwd.encode()).hexdigest().lower() == self.password

    def display_name(self) -> str:
        """Return the display name based on email, first_name, and last_name"""
        if not self.email and not self.first_name and not self.last_name:
            return ""
        if not self.first_name and not self.last_name:
            return f"{self.email}"
        if not self.last_name:
            return f"{self.first_name}"
        if not self.first_name:
            return f"{self.last_name}"
        return f"{self.first_name} {self.last_name}"

    def to_json(self, for_serialization: bool = False) -> dict:
        """Return a JSON-serializable representation of the User object"""
        # Start by getting the base class's to_json result
        result = super().to_json(for_serialization=for_serialization)

        # Customize the result as needed
        if 'logs' in result:  # Remove relationships if necessary
            del result['logs']
        if 'tags' in result:
            del result['tags']

        # Example: Format datetime fields
        if 'account_created_at' in result and isinstance(result['account_created_at'], datetime):
            result['account_created_at'] = result['account_created_at'].strftime(
                TIMESTAMP_FORMAT)
        if 'last_login' in result and isinstance(result['last_login'], datetime):
            result['last_login'] = result['last_login'].strftime(
                TIMESTAMP_FORMAT)

        # Handle or exclude any other SQLAlchemy internals
        result = {k: v for k, v in result.items()}

        return result
