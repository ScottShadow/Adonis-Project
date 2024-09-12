from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, Session
from .base import Base as SQLAlchemyBase, BaseClass
from user import User
from tag import Tag

class UserTag(BaseClass, SQLAlchemyBase):
    __tablename__ = 'user_tags'
    user_id = Column(String(36), ForeignKey('users.id'), primary_key=True)
    tag_id = Column(String(36), ForeignKey('tags.id'), primary_key=True)


    user = relationship('User', back_populates='user_tags')
    tag = relationship('Tag', back_populates='user_tags')

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