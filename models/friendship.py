from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .base import Base as SQLAlchemyBase, BaseClass


class Friendship(BaseClass, SQLAlchemyBase):
    """ Friendship model to handle user relationships """
    __tablename__ = 'friendships'

    user_id_1 = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_id_2 = Column(Integer, ForeignKey('users.id'), nullable=False)
    # e.g., pending, accepted, blocked
    status = Column(String(50), nullable=False)
    # Friends can view each other's logs by default
    can_view_logs = Column(Boolean, default=True)

    user_1 = relationship('User', foreign_keys=user_id_1,
                          back_populates='friendships_1')
    user_2 = relationship('User', foreign_keys=user_id_2,
                          back_populates='friendships_2')

    def __repr__(self):
        return f"<Friendship(id={self.id}, user_id_1={self.user_id_1}, user_id_2={self.user_id_2}, status='{self.status}')>"
