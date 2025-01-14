from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime, func, Index, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
from .base import Base as SQLAlchemyBase, BaseClass


class FriendshipStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    BLOCKED = "blocked"


class Friendship(BaseClass, SQLAlchemyBase):
    """ Friendship model to handle user relationships """
    __tablename__ = 'friendships'

    user_id_1 = Column(String(36), ForeignKey('users.id'),
                       nullable=False,)
    user_id_2 = Column(String(36), ForeignKey('users.id'), nullable=False)

    status = Column(Enum(FriendshipStatus), nullable=False,
                    default=FriendshipStatus.PENDING)
    can_view_logs = Column(Boolean, default=True)

    user_1 = relationship('User', foreign_keys=user_id_1,
                          back_populates='friendships_1', overlaps="friends")
    user_2 = relationship('User', foreign_keys=user_id_2,
                          back_populates='friendships_2', overlaps="friends")

    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id_1 = kwargs.get('user_id_1')
        self.user_id_2 = kwargs.get('user_id_2')
        self.status = kwargs.get('status', FriendshipStatus.PENDING)
        self.can_view_logs = kwargs.get('can_view_logs', True)

    def __repr__(self):
        return f"<Friendship(id={self.id}, user_id_1={self.user_id_1}, user_id_2={self.user_id_2}, status='{self.status}')>"
