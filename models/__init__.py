# models/__init__.py

from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, func
from models.base import Base as SQLAlchemyBase

user_tags = Table(
    'user_tags', SQLAlchemyBase.metadata,
    Column('user_id', String(36), ForeignKey('users.id'), primary_key=True),
    Column('tag_id', String(36), ForeignKey('tags.id'), primary_key=True)
)

from models.user import User
from models.log import Log
#from models.friendship import Friendship
from models.tag import Tag
from models.user_session import UserSession

