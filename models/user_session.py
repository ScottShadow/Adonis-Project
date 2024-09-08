#!/usr/bin/env python3
""" UserSession module"""
from models.base import Base as SQLAlchemyBase, BaseClass, SessionLocal
from sqlalchemy import Column, String
from datetime import datetime


class UserSession(BaseClass, SQLAlchemyBase):
    """ UserSession model to store user sessions """
    __tablename__ = 'user_sessions'  # Define the table name in the database

    user_id = Column(String(36), nullable=False)
    session_id = Column(String(36), nullable=False)

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize UserSession instance with user_id and session_id """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

    def save(self):
        """Save the UserSession instance to the MySQL database."""
        session = SessionLocal()
        try:
            # If the instance does not have an ID, use the session_id (or generate one)
            if not hasattr(self, 'id'):
                self.id = self.session_id  # Assuming session_id exists and is unique

            # Add the object to the session
            session.add(self)

            # Commit the changes to the database
            session.commit()
        except Exception as e:
            session.rollback()  # Rollback in case of an error
            raise e
        finally:
            session.close()

    def remove(self):
        """Remove the UserSession instance from the MySQL database."""
        session = SessionLocal()
        try:
            # If the instance has an ID, remove it from the database
            if hasattr(self, 'id'):
                # Find the object in the database by ID
                session_obj = session.query(UserSession).get(self.id)

                # If the object exists, delete it
                if session_obj:
                    session.delete(session_obj)

                    # Commit the changes to the database
                    session.commit()
        except Exception as e:
            session.rollback()  # Rollback in case of an error
            raise e
        finally:
            session.close()

    def save_datafile(self):
        """ Save the UserSession instance to the DATA dictionary """
        if not hasattr(self, 'id'):
            self.id = self.session_id
        super().save()

    def remove_datafile(self):
        """ Remove the UserSession instance from the DATA dictionary """
        if hasattr(self, 'id'):
            del DATA[UserSession.__name__][self.id]
