# db_setup.py

# Import Base and engine from the base model
from models.base import Base, engine
from models.user import User
from models.user_session import UserSession
# from models.friendship import Friendship
from models.log import Log
from models.tag import Tag


def init_db():
    """
    Initializes the database by creating all tables defined in the Base metadata.
    """
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    # Run this script to initialize the database
    init_db()
    print("Database tables created!")
