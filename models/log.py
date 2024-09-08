from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base, SessionLocal
from models.user import User
from .base import Base as SQLAlchemyBase, BaseClass
from models.models_helper import calculate_xp


class Log(BaseClass, SQLAlchemyBase):
    __tablename__ = 'logs'

    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    # e.g., 'Exercise', 'Reading'
    habit_type = Column(String(50), nullable=False)
    habit_name = Column(String(100), nullable=False)  # e.g., 'Morning Run'
    # Optional field for extra context
    log_details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
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
    # Relationship with Tags - assuming a Many-to-Many relationship
    tags = relationship(
        'Tag', secondary='log_tags', back_populates='logs')

    # Define relationships
    user = relationship('User', back_populates='logs')

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a Log instance."""
        super().__init__(*args, **kwargs)

        # Required fields
        self.user_id = kwargs.get('user_id')
        if not self.user_id:
            raise ValueError("User ID is required for Log creation")

        self.habit_type = kwargs.get('habit_type')
        if not self.habit_type:
            raise ValueError("Habit Type is required for Log creation")

        self.habit_name = kwargs.get('habit_name')
        if not self.habit_name:
            raise ValueError("Habit Name is required for Log creation")

        # Optional fields with default values
        self.log_details = kwargs.get('log_details', None)
        self.xp = kwargs.get('xp', calculate_xp(self))
        self.source = kwargs.get('source', 'Manual')
        self.status = kwargs.get('status', 'Completed')
        self.visibility = kwargs.get('visibility', 'Private')
        self.shared_with = kwargs.get('shared_with', None)

        self.update_user_xp()

    def update_user_xp(self):
        """Update the associated user's XP."""
        session = SessionLocal()  # Get a new session
        try:
            user = session.query(User).get(self.user_id)
            if user:
                user.total_xp += self.xp  # Update the user's XP
                print(
                    f"[DEBUG]Updated user {user.id} with {self.xp} XP now is {user.total_xp}")
                session.commit()  # Save changes to the database
        except Exception as e:
            session.rollback()  # Rollback if an error occurs
            raise e
        finally:
            session.close()  # Close the session

    def __repr__(self):
        return f"<Log(habit_name='{self.habit_name}', user_id={self.user_id}, timestamp={self.timestamp})>"
