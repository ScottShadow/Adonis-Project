# models/__init__.py

from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, func
from models.base import Base


room_members = Table('room_members', Base.metadata,
    Column('user_id', String(36), ForeignKey('users.id')),
    Column('room_id', String(36), ForeignKey('rooms.id'))
)

from models.user import User
from models.log import Log
#from models.friendship import Friendship
from models.tag import Tag
from models.user_session import UserSession
from models.user_tag import UserTag
from models.room import Room
from models.message import Message

