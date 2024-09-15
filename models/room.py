from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base, SessionLocal
from .base import Base as SQLAlchemyBase, BaseClass
# from models.models_helper import *
from datetime import datetime


class Room(BaseClass, SQLAlchemyBase):
    __tablename__ = 'rooms'

    name = Column(String(250), nullable=False)
    # False for global/group rooms, True for DMs
    is_dm = Column(Boolean, default=False)

    # Relationships
    messages = relationship('Message', backref='room',
                            order_by="Message.created_at.asc()", lazy=True)
    users = relationship('User', secondary='room_members',
                         back_populates='rooms')

    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.name = kwargs.get('name')
        self.is_dm = kwargs.get('is_dm')

    def __repr__(self):
        return f"<Room(id={self.id}, name='{self.name}')>, created_at={self.created_at}"
