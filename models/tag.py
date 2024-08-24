from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base as SQLAlchemyBase, BaseClass

# Association Table for the many-to-many relationship between Tags and Logs
tag_logs = Table(
    'tag_logs', SQLAlchemyBase.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
    Column('log_id', Integer, ForeignKey('logs.id'), primary_key=True)
)

# Association Table for the many-to-many relationship between Tags and Users
user_tags = Table(
    'user_tags', SQLAlchemyBase.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)


class Tag(SQLAlchemyBase, BaseClass):
    """Tag model to represent tags/skills that can be assigned to users and 
    linked to logs."""
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(250), nullable=False,
                  unique=True)  # Name of the tag/skill
    # Optional description of the tag/skill
    description = Column(String(500), nullable=True)
    # Assumes level is stored as an integer
    level = Column(Integer, nullable=True)

    # Relationships
    users = relationship('User', secondary=user_tags, back_populates='tags')
    logs = relationship('Log', secondary=tag_logs, back_populates='tags')

    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}')>"
