#!/usr/bin/env python3
"""Combined User Model Module"""
import hashlib
from .base import Base as SQLAlchemyBase, BaseClass

from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, func
from sqlalchemy.orm import relationship


# Many-to-Many relationship table for users and tags
user_tags = Table(
    'user_tags', SQLAlchemyBase.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class User(SQLAlchemyBase, BaseClass):
    """Combined User class using SQLAlchemy and custom methods"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String(250), nullable=False, unique=True)
    username = Column(String(250), nullable=False,
                      unique=True)  # User's chosen name
    _hashed_password = Column("hashed_password", String(250), nullable=False)
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
    account_created_at = Column(DateTime, default=func.now)
    last_login = Column(DateTime, nullable=True)  # Last login timestamp

    # Relationships
    logs = relationship('Log', back_populates='user',
                        cascade="all, delete-orphan")
    friends = relationship(
        'User',
        secondary='friendships',
        primaryjoin='User.id == Friendship.user_id_1',
        secondaryjoin='User.id == Friendship.user_id_2',
        backref=backref('friendships', cascade='all, delete-orphan')
    )
    tags = relationship('Tag', secondary='user_tags', back_populates='users')

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"

    def __init__(self, email: str, password: str, first_name: str = None, last_name: str = None):
        """Initialize a User instance"""
        self.email = email
        self.password = password  # This will invoke the password setter
        self.first_name = first_name
        self.last_name = last_name

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
