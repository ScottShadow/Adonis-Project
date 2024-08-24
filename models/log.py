from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base
from .base import Base as SQLAlchemyBase, BaseClass


class Log(SQLAlchemyBase, BaseClass):
    __tablename__ = 'logs'

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # e.g., 'Exercise', 'Reading'
    habit_type = Column(String(50), nullable=False)
    habit_name = Column(String(100), nullable=False)  # e.g., 'Morning Run'
    # Optional field for extra context
    log_details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=func.now, nullable=False)
    # Experience Points, optional
    xp = Column(Integer, nullable=True, default=0)
    # e.g., 'Manual', 'Quick Log', 'API'
    source = Column(String(50), nullable=True)
    status = Column(Enum('Completed', 'Pending', 'Scheduled',
                    name='log_status'), nullable=True)
    visibility = Column(Enum('Private', 'Friends', 'Clan', 'Public',
                        name='log_visibility'), nullable=False, default='Private')
    # Optional, can store user IDs or groups
    shared_with = Column(Text, nullable=True)
    # Relationship with Tags/Skills - assuming a Many-to-Many relationship
    tags_skills = relationship(
        'TagSkill', secondary='log_tagskills', back_populates='logs')

    # Define relationships
    user = relationship('User', back_populates='logs')

    def __init__(self, user_id, habit_type, habit_name, log_details=None, xp=0, source='Manual', status='Completed', visibility='Private', shared_with=None):
        self.user_id = user_id
        self.habit_type = habit_type
        self.habit_name = habit_name
        self.log_details = log_details
        self.xp = xp
        self.source = source
        self.status = status
        self.visibility = visibility
        self.shared_with = shared_with

    def __repr__(self):
        return f"<Log(habit_name='{self.habit_name}', user_id={self.user_id}, timestamp={self.timestamp})>"
