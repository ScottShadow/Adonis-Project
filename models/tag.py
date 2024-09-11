from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base as SQLAlchemyBase, BaseClass
from models import user_tags


# Association Table for the many-to-many relationship between Tags and Logs
log_tags = Table(
    'log_tags', SQLAlchemyBase.metadata,
    Column('tag_id', String(36), ForeignKey('tags.id'), primary_key=True),
    Column('log_id', String(36), ForeignKey('logs.id'), primary_key=True)
)


class Tag(BaseClass, SQLAlchemyBase):
    """Tag model to represent tags/skills that can be assigned to users and
    linked to logs."""
    __tablename__ = "tags"

    name = Column(String(250), nullable=False,
                  unique=True)  # Name of the tag/skill
    # category tag belongs to
    category = Column(String(250), nullable=False)
    # Optional description of the tag/skill
    description = Column(String(500), nullable=True)
    # Assumes level is stored as an integer
    level = Column(Integer, nullable=True)

    # Relationships
    users = relationship('User', secondary=user_tags, back_populates='tags')
    logs = relationship('Log', secondary=log_tags, back_populates='tags')

    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}')>"

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a User instance"""
        super().__init__(*args, **kwargs)

        self.name = kwargs.get('name')
        if not self.name:
            raise ValueError("Name is required for Tag creation")

        self.category = kwargs.get('category')
        if not self.category:
            raise ValueError("Category is required for Tag creation")

        self.description = kwargs.get('description', None)

        self.level = kwargs.get('level', 0)
