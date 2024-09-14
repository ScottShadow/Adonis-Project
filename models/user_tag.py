from sqlalchemy import Column, String, ForeignKey, Table, DateTime, func
from sqlalchemy.orm import relationship, Session, SessionLocal
from models.base import Base as SQLAlchemyBase, BaseClass
from models.tag import User
from models.tag import Tag
from models.log import Log

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"

class UserTag(BaseClass, SQLAlchemyBase):
    __tablename__ = 'user_tags'
    user_id = Column(String(36), ForeignKey('users.id'), primary_key=True)
    tag_id = Column(String(36), ForeignKey('tags.id'), primary_key=True)


    user = relationship('User', back_populates='user_tags')
    tag = relationship('Tag', back_populates='user_tags')
    
    def __init__(self, user_id: str, tag_id: str):
        """Initialize a UserTag instance."""
        self.user_id = user_id
        self.tag_id = tag_id

    def __repr__(self):
        """Return a string representation of the UserTag instance."""
        return f"<UserTag(user_id='{self.user_id}', tag_id='{self.tag_id}')>"

    def add_tag_to_user(session: Session, user_id: str, tag_name: str):
        """Add a tag to the user profile."""
        user = session.query(User).filter(User.id == user_id).one_or_none()
        tag = session.query(Tag).filter(Tag.name == tag_name).one_or_none()

        if not user:
            print(f"User with id '{user_id}' not found.")
            return
        if not tag:
            print(f"Tag with name '{tag_name}' not found.")
            return

        existing_user_tag = session.query(UserTag).filter_by(user_id=user.id, tag_id=tag.id).one_or_none()
        if existing_user_tag:
            print(f"User already has the tag '{tag_name}'.")
            return

        user_tag = UserTag(user_id=user.id, tag_id=tag.id)
        session.add(user_tag)
        session.commit()

        print(f"Added tag '{tag_name}' to user with id '{user_id}'.")

    def remove_tag_from_user(session: Session, user_id: str, tag_name: str):
        """Remove a tag from the user profile."""
        user = session.query(User).filter(User.id == user_id).one_or_none()
        tag = session.query(Tag).filter(Tag.name == tag_name).one_or_none()

        if not user:
            print(f"User with id '{user_id}' not found.")
            return
        if not tag:
            print(f"Tag with name '{tag_name}' not found.")
            return

        user_tag = session.query(UserTag).filter_by(user_id=user.id, tag_id=tag.id).one_or_none()
        if not user_tag:
            print(f"User does not have the tag '{tag_name}'.")
            return

        session.delete(user_tag)
        session.commit()

        print(f"Removed tag '{tag_name}' from user with id '{user_id}'.")

    def to_json(self, for_serialization: bool = False) -> dict:
        """Return a JSON-serializable representation of the UserTag object"""
        # Start with the base class's to_json result
        result = super().to_json(for_serialization=for_serialization)

        # Customize the result
        if 'user' in result:
            del result['user']  # Remove the user relationship
        if 'tag' in result:
            del result['tag']  # Remove the tag relationship

        # Example: Format datetime fields if present
        if 'created_at' in result and isinstance(result['created_at'], datetime):
            result['created_at'] = result['created_at'].strftime(TIMESTAMP_FORMAT)
        if 'updated_at' in result and isinstance(result['updated_at'], datetime):
            result['updated_at'] = result['updated_at'].strftime(TIMESTAMP_FORMAT)

        # Ensure no SQLAlchemy internals are present
        result = {k: v for k, v in result.items() if not isinstance(v, Session)}

        return result
