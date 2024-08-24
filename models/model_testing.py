# Let's start by setting up the models you provided and inheriting from the given BaseClass. Then, we'll implement some simple tests to verify that the models are functioning correctly.

from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Assuming the BaseClass provided by the user
from datetime import datetime
from typing import TypeVar, List, Iterable
from os import path
import json
import uuid

Base = declarative_base()

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA = {}


class BaseClass:
    """ Base class """
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_at = Column(
        String, default=datetime.utcnow().strftime(TIMESTAMP_FORMAT))
    updated_at = Column(
        String, default=datetime.utcnow().strftime(TIMESTAMP_FORMAT))

    def __init__(self, *args: list, **kwargs: dict):
        s_class = str(self.__class__.__name__)
        if DATA.get(s_class) is None:
            DATA[s_class] = {}

        if kwargs.get('id') is not None:
            self.id = kwargs.get('id')
        if kwargs.get('created_at') is not None:
            self.created_at = kwargs.get('created_at')
        if kwargs.get('updated_at') is not None:
            self.updated_at = kwargs.get('updated_at')

    def save(self):
        s_class = self.__class__.__name__
        DATA[s_class][self.id] = self

    def __eq__(self, other: TypeVar('Base')) -> bool:
        if not isinstance(other, BaseClass):
            return False
        return self.id == other.id

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

# Models setup


# Association Table for the many-to-many relationship between Tags and Logs
tag_logs = Table(
    'tag_logs', Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
    Column('log_id', Integer, ForeignKey('logs.id'), primary_key=True)
)

# Association Table for the many-to-many relationship between Tags and Users
user_tags = Table(
    'user_tags', Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)


class User(BaseClass, Base):
    __tablename__ = "users"

    email = Column(String(250), nullable=False, unique=True)
    _hashed_password = Column("hashed_password", String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
    first_name = Column(String(250), nullable=True)
    last_name = Column(String(250), nullable=True)

    logs = relationship('Log', back_populates='user',
                        cascade="all, delete-orphan")
    friends = relationship('User', secondary='friendships', primaryjoin=id == ForeignKey('friendships.user_id'),
                           secondaryjoin=id == ForeignKey('friendships.friend_id'), back_populates='friends')
    tags = relationship('Tag', secondary=user_tags, back_populates='users')


class Tag(BaseClass, Base):
    __tablename__ = "tags"

    name = Column(String(250), nullable=False, unique=True)
    description = Column(String(500), nullable=True)

    users = relationship('User', secondary=user_tags, back_populates='tags')
    logs = relationship('Log', secondary=tag_logs, back_populates='tags')


class Log(BaseClass, Base):
    __tablename__ = "logs"

    user_id = Column(Integer, ForeignKey('users.id'))
    habit_type = Column(String(250), nullable=False)
    habit_name = Column(String(250), nullable=False)
    log_details = Column(String(500), nullable=True)
    timestamp = Column(
        String, default=datetime.utcnow().strftime(TIMESTAMP_FORMAT))
    xp = Column(Integer, default=0)
    source = Column(String(250), nullable=True)
    status = Column(String(250), nullable=True)
    visibility = Column(String(250), nullable=False)
    shared_with = Column(String(250), nullable=True)

    user = relationship('User', back_populates='logs')
    tags = relationship('Tag', secondary=tag_logs, back_populates='logs')


# Database setup for testing
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Simple tests


def test_create_user():
    user = User(email="test@example.com", _hashed_password="hashed_password",
                first_name="Test", last_name="User")
    session.add(user)
    session.commit()
    retrieved_user = session.query(User).filter_by(
        email="test@example.com").first()
    assert retrieved_user is not None, "User creation failed!"
    assert retrieved_user.email == "test@example.com", "Email mismatch!"
    print("User creation test passed!")


def test_create_tag():
    tag = Tag(name="Test Tag", description="A test tag for activities.")
    session.add(tag)
    session.commit()
    retrieved_tag = session.query(Tag).filter_by(name="Test Tag").first()
    assert retrieved_tag is not None, "Tag creation failed!"
    assert retrieved_tag.name == "Test Tag", "Tag name mismatch!"
    print("Tag creation test passed!")


def test_create_log():
    user = session.query(User).filter_by(email="test@example.com").first()
    tag = session.query(Tag).filter_by(name="Test Tag").first()
    log = Log(user_id=user.id, habit_type="Exercise",
              habit_name="Morning Run", xp=100, visibility="Public")
    log.tags.append(tag)
    session.add(log)
    session.commit()
    retrieved_log = session.query(Log).filter_by(
        habit_name="Morning Run").first()
    assert retrieved_log is not None, "Log creation failed!"
    assert retrieved_log.habit_name == "Morning Run", "Habit name mismatch!"
    assert retrieved_log.tags[0].name == "Test Tag", "Tag assignment failed!"
    print("Log creation test passed!")


# Running the tests
test_create_user()
test_create_tag()
test_create_log()
