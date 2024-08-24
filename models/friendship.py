from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .base import Base as SQLAlchemyBase, BaseClass


class Friendship(SQLAlchemyBase, BaseClass):
    """ Friendship model to handle user relationships """
    __tablename__ = 'friendships'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id_1 = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_id_2 = Column(Integer, ForeignKey('users.id'), nullable=False)
    # e.g., pending, accepted, blocked
    status = Column(String(50), nullable=False)
    # Friends can view each other's logs by default
    can_view_logs = Column(Boolean, default=True)
    # Timestamp for when the friendship was initiated
    created_at = Column(DateTime, default=func.now)
    # Timestamp for the last status update
    updated_at = Column(DateTime, onupdate=func.now)

    user_1 = relationship("User", foreign_keys=[user_id_1])
    user_2 = relationship("User", foreign_keys=[user_id_2])

    def __repr__(self):
        return f"<Friendship(id={self.id}, user_id_1={self.user_id_1}, user_id_2={self.user_id_2}, status='{self.status}')>"
