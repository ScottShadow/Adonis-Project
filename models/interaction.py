from sqlalchemy import Column, String, Enum, String, TIMESTAMP, ForeignKey, UniqueConstraint, Text
from sqlalchemy.orm import relationship, remote
from .base import Base as SQLAlchemyBase, BaseClass
import enum


class EntityType(enum.Enum):
    HABIT_LOG = "habit_log"
    POST = "post"
    COMMENT = "comment"
    EVENT = "event"


class Comment(BaseClass, SQLAlchemyBase):
    """Comment model for handling nested comments with polymorphic entities."""
    __tablename__ = "comments"

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"),
                     nullable=False)  # Who commented
    entity_id = Column(String(36),
                       nullable=False)  # What was commented on
    # Where it was posted
    entity_type = Column(Enum(EntityType), nullable=False)
    text = Column(Text, nullable=False)  # Comment content
    # NULL = top-level comment, Otherwise = reply
    parent_id = Column(String(36), ForeignKey('comments.id'), nullable=True)

    # Relationships
    replies = relationship("Comment", backref="parent",
                           primaryjoin="foreign(Comment.parent_id) == remote(Comment.id)")  # Nested comments
    reactions = relationship(
        "Reaction", primaryjoin="and_(foreign(Reaction.entity_id) == Comment.id, Reaction.entity_type == 'EntityType.COMMENT')",
        backref="comment", lazy="joined")

    def __repr__(self):
        return f"<Comment(id={self.id}, user_id={self.user_id}, entity_type={self.entity_type})>"

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a Comment instance."""
        super().__init__(*args, **kwargs)

        self.user_id = kwargs.get('user_id')
        if not self.user_id:
            raise ValueError("User ID is required for Comment creation")

        self.entity_id = kwargs.get('entity_id')
        if not self.entity_id:
            raise ValueError("Entity ID is required for Comment creation")

        self.entity_type = kwargs.get('entity_type')
        if not self.entity_type:
            raise ValueError("Entity type is required for Comment creation")

        self.text = kwargs.get('text')
        if not self.text:
            raise ValueError("Text content is required for Comment creation")

        self.parent_id = kwargs.get('parent_id', None)  # Optional nesting


class ReactionType(enum.Enum):
    MOTIVATED = "motivated"
    INSPIRED = "inspired"
    EDUCATED = "educated"


class Reaction(BaseClass, SQLAlchemyBase):
    """Reaction model for supporting different reactions on logs, posts, comments, and events."""

    __tablename__ = "reactions"

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"),
                     nullable=False)  # Who reacted
    entity_id = Column(String(36), nullable=False)  # What was reacted to
    # Type of entity (log, post, comment)
    entity_type = Column(Enum(EntityType), nullable=False)
    # Type of reaction (motivated, inspired, etc.)
    reaction_type = Column(Enum(ReactionType), nullable=False)

    # Relationships (optional, depending on how you fetch reactions)

    # Optional: Establish relationships for different reaction targets
    # log = relationship("Log", primaryjoin="and_(foreign(Reaction.entity_id) == Log.id, Reaction.entity_type == 'EntityType.HABIT_LOG')",
    #                    back_populates="reactions", lazy="joined")
    # post = relationship("Post", primaryjoin="and_(Reaction.entity_id == Post.id, Reaction.entity_type == 'EntityType.POST')",
    #                     backref="reactions", lazy="joined")

    # Prevent duplicate reactions by the same user on the same entity
    # __table_args__ = (UniqueConstraint('user_id', 'entity_id',
    #                                    'entity_type', name='unique_reaction'),)

    def __repr__(self):
        return f"<Reaction(id={self.id}, user_id={self.user_id}, entity_type={self.entity_type}, reaction_type={self.reaction_type})>"

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a Reaction instance."""
        super().__init__(*args, **kwargs)

        self.user_id = kwargs.get('user_id')
        if not self.user_id:
            raise ValueError("User ID is required for Reaction creation")

        self.entity_id = kwargs.get('entity_id')
        if not self.entity_id:
            raise ValueError("Entity ID is required for Reaction creation")

        self.entity_type = kwargs.get('entity_type')
        if not self.entity_type:
            raise ValueError("Entity type is required for Reaction creation")

        self.reaction_type = kwargs.get('reaction_type')
        if not self.reaction_type:
            raise ValueError("Reaction type is required for Reaction creation")
