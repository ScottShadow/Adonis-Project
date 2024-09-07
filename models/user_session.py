#!/usr/bin/env python3
""" UserSession module"""
from models.base import Base as SQLAlchemyBase, BaseClass
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
        """ Save the UserSession instance to the DATA dictionary """
        if not hasattr(self, 'id'):
            self.id = self.session_id
        super().save()

    def remove(self):
        """ Remove the UserSession instance from the DATA dictionary """
        if hasattr(self, 'id'):
            del DATA[UserSession.__name__][self.id]
