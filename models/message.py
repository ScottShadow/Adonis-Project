from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base, SessionLocal
from .base import Base as SQLAlchemyBase, BaseClass
# from models.models_helper import *
from datetime import datetime


class Message(BaseClass, SQLAlchemyBase):
    __tablename__ = 'messages'

    room_id = Column(String(36), ForeignKey('rooms.id'), nullable=False)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    content = Column(String(500), nullable=False)

    # Relationships
    user = relationship('User', backref='messages')
    # room = relationship('Room', backref='messages')

    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.room_id = kwargs.get('room_id')
        self.user_id = kwargs.get('user_id')
        self.content = kwargs.get('content')

    def __repr__(self):
        return f"<Message(id={self.id}, room_id={self.room_id}, user_id={self.user_id}, content='{self.content}')>"
