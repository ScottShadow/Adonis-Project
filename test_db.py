# test_db.py

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError

# Database configuration (without specifying the database name)
DATABASE_URL = "mysql://root:56213@localhost/"

# Database name
db_name = "adonis_db"

# Create an engine for MySQL without specifying a database
engine = create_engine(DATABASE_URL)

# Function to create the database if it doesn't exist


def create_database(engine, db_name):
    conn = engine.connect()
    try:
        # Use `text()` to wrap the raw SQL query
        conn.execute(text(f"CREATE DATABASE {db_name}"))
        print(f"Database '{db_name}' created successfully.")
    except ProgrammingError as e:
        if f"Can't create database '{db_name}'" in str(e):
            print(f"Database '{db_name}' already exists.")
        else:
            print(f"Error: {e}")
    finally:
        conn.close()


# Call the function to create the database if needed
create_database(engine, db_name)

# Once the database exists, you can create an engine bound to that database
DATABASE_URL_WITH_DB = f"mysql://root:56213@localhost/{db_name}"
engine_with_db = create_engine(DATABASE_URL_WITH_DB, echo=True)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_with_db)

Base = declarative_base()

# Define a simple model to test


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

# Create the tables in the database


def init_db():
    # Use the correct engine here
    Base.metadata.create_all(bind=engine_with_db)

# Function to test inserting and fetching data


def test_db():
    session = SessionLocal()

    # Create a new user
    new_user = User(name="Test User")
    session.add(new_user)
    session.commit()

    # Fetch all users
    users = session.query(User).all()
    print(users)

    session.close()


if __name__ == "__main__":
    init_db()   # Create the table
    test_db()   # Test the insert and query
