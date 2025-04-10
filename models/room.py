from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean, Enum, UUID, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base, SessionLocal
from .base import Base as SQLAlchemyBase, BaseClass
# from models.models_helper import *
from datetime import datetime
import enum


class RoomTypes(enum.Enum):
    CIRCLE = "circle"
    COMMENT = "comment"
    CHAT = "chat"


class EventTypes(enum.Enum):
    POST = "post"
    COMMENT = "comment"
    REACTION = "reaction"
    MESSAGE = "message"
    FRIEND_REQUEST = "friend_request"


room_types = Enum('circle', 'comment', 'chat', name='room_types')
event_types = Enum(
    'post', 'comment', 'reaction', 'message', name='event_types')


class Room(BaseClass, SQLAlchemyBase):
    """Room model for managing chat rooms and their members.

    Attributes:
        name (str): Name of the room
        type (Enum): Type of room (circle, comment, chat)
        is_dm (bool): True for direct messages, False for group rooms
        messages (list): List of messages in the room
        users (list): List of user subscriptions
        events (list): List of notification events
    """
    __tablename__ = 'rooms'

    name = Column(String(250), nullable=False)
    type = Column(Enum(RoomTypes), nullable=True)
    # False for global/group rooms, True for DMs
    is_dm = Column(Boolean, default=False)

    # Relationships
    messages = relationship('Message', backref='room',
                            order_by="Message.created_at.asc()", lazy=True)
    # users = relationship('User', secondary='room_members',back_populates='rooms')
    users = relationship("UserSubscription",
                         back_populates="room", cascade="all, delete-orphan")

    events = relationship("NotificationEvent", back_populates="room")

    user_read_status = relationship("ActivityStatus", back_populates="room")

    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.name = kwargs.get('name')
        self.is_dm = kwargs.get('is_dm')
        self.type = kwargs.get('type')

    def __repr__(self):
        return f"<Room(id={self.id}, name='{self.name}')>, created_at={self.created_at}"


class NotificationEvent(BaseClass, SQLAlchemyBase):
    """Model for tracking notification events in rooms.

    Attributes:
        room_id (str): ID of the room where event occurred
        event_type (Enum): Type of event (new_post, new_comment, new_reaction)
        actor_id (str): ID of user who triggered the event
        content (dict): Additional event data (post_id, comment_id, etc.)
        room (Room): Related room
        statuses (list): List of notification statuses
    """
    __tablename__ = "notification_events"

    room_id = Column(String(36), ForeignKey("rooms.id"), nullable=False)
    event_type = Column(Enum(EventTypes), nullable=True)
    actor_id = Column(String(36), ForeignKey(
        "users.id"))  # Who triggered it
    # Stores extra info (post_id, comment_id, etc.)
    content = Column(JSON, nullable=True)
    url = Column(String(120), nullable=True)

    # Relationships
    room = relationship("Room", back_populates="events")
    # statuses = relationship("NotificationStatus", back_populates="event")

    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.room_id = kwargs.get('room_id')
        self.event_type = kwargs.get('event_type')
        self.actor_id = kwargs.get('actor_id')
        self.content = kwargs.get('content')

    def __repr__(self):
        return f"<NotificationEvent(id={self.id}, room_id={self.room_id}, event_type={self.event_type}, created_at={self.created_at}, actor_id={self.actor_id}, content={self.content})>"


class ActivityStatus(BaseClass, SQLAlchemyBase):
    """Model for tracking user activity in rooms, for notifications.

    Attributes:
        user_id (str): ID of the user
        room_id (str): ID of the room
        last_seen_at (datetime): When the notification was seen
        user (User): Related user
        event (NotificationEvent): Related event
    """
    __tablename__ = "activity_status"

    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    room_id = Column(String(36), ForeignKey("rooms.id"), nullable=False)

    __table_args__ = (UniqueConstraint(
        'user_id', 'room_id', name='unique_user_seen_status'),)
    # Relationships
    user = relationship("User", back_populates="read_status")
    room = relationship("Room", back_populates="user_read_status")

    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.room_id = kwargs.get('room_id')
        self.last_seen_at = kwargs.get('seen_at')

    def __repr__(self):
        return f"<ActivityStatus(user_id={self.user_id}, event_id={self.room_id}, seen_at={self.seen_at})>"


class NotificationStatus(BaseClass, SQLAlchemyBase):
    """Model for tracking user notification status in rooms.

    Attributes:
        user_id (str): ID of the user
        event_id (str): ID of the notification event
        seen_at (datetime): When the notification was seen
        user (User): Related user
        event (NotificationEvent): Related event
    """
    __tablename__ = "notification_status"

    user_id = Column(String(36), ForeignKey("users.id"))
    event_id = Column(String(36), ForeignKey("notification_events.id"))
    seen_at = Column(DateTime, nullable=True)

    __table_args__ = (UniqueConstraint(
        'user_id', 'event_id', name='unique_user_notification_status'),)
    # Relationships
    # user = relationship("User", back_populates="notification_statuses")
    # event = relationship("NotificationEvent", back_populates="statuses")

    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.event_id = kwargs.get('event_id')
        self.seen_at = kwargs.get('seen_at')

    def __repr__(self):
        return f"<NotificationStatus(user_id={self.user_id}, event_id={self.event_id}, seen_at={self.seen_at})>"


class UserSubscription(BaseClass, SQLAlchemyBase):
    """Model for managing user subscriptions to rooms.

    Attributes:
        user_id (str): ID of the subscribed user
        room_id (str): ID of the room
        subscribed_at (datetime): When the subscription was created
        is_muted (bool): Whether notifications are muted
        user (User): Related user
        room (Room): Related room
    """
    __tablename__ = "user_subscriptions"

    user_id = Column(String(36), ForeignKey("users.id"))
    room_id = Column(String(36), ForeignKey("rooms.id"))
    is_muted = Column(Boolean, default=False)

    # Add a unique constraint instead to ensure no duplicate subscriptions
    __table_args__ = (UniqueConstraint(
        'user_id', 'room_id', name='unique_user_room'),)

    # Relationships
    user = relationship("User", back_populates="subscriptions")
    room = relationship("Room", back_populates="users")

    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.room_id = kwargs.get('room_id')
        self.subscribed_at = kwargs.get('subscribed_at', datetime.utcnow())
        self.is_muted = kwargs.get('is_muted', False)

    def __repr__(self):
        return f"<UserSubscription(user_id={self.user_id}, room_id={self.room_id}, subscribed_at={self.subscribed_at}, is_muted={self.is_muted})>"
