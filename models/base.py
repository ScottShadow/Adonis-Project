#!/usr/bin/env python3
""" Base module with mysql database
"""
from datetime import datetime
from typing import TypeVar, List, Iterable
from os import path
import os
import json
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, text, and_, func
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, func
from sqlalchemy.exc import ProgrammingError

# Environment variables from Docker compose
DB_USER = os.getenv('DB_USER', 'root')
print(f"DB_USER: {DB_USER}")
DB_PASSWORD = os.getenv('DB_PASSWORD', '56213')
DB_PASSWORD = "vLWABIdIsyImdWEqBhXOHefpSDfbudRy"
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_HOST = "mysql.railway.internal"
print(f"DB_HOST: {DB_HOST}")
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'adonis_db')
DB_NAME = "railway"
# Database configuration (without specifying the database name)
DATABASE_URL = os.getenv(
    "DATABASE_URL", "mysql://root:56213@localhost/{DB_NAME}".format(DB_NAME=DB_NAME))
DATABASE_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@junction.proxy.rlwy.net:50075/{DB_NAME}"
print(f"DATABASE_URL: {DATABASE_URL}")

# Create an engine for MySQL without specifying a database
engine = create_engine(DATABASE_URL, echo=True)

# Function to create the database if it doesn't exist


def create_database(current_engine, db_name):

    try:
        conn = current_engine.connect()
        # Use `text()` to wrap the raw SQL query
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
        print(f"Database '{db_name}' created successfully.")
    except ProgrammingError as e:
        if f"Can't create database '{db_name}'" in str(e):
            print(f"Database '{db_name}' already exists.")
        else:
            print(f"Error: {e}")
    finally:
        conn.close()


# Call the function to create the database if needed
# create_database(engine, DB_NAME)

# Once the database exists, you can create an engine bound to that database
# DATABASE_URL_WITH_DB = f"{DATABASE_URL}{DB_NAME}"
# engine_with_db = create_engine(DATABASE_URL_WITH_DB, echo=False)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA = {}


class BaseClass():
    """Base class that other models will inherit from"""
    __abstract__ = True  # This tells SQLAlchemy not to create a table for this class

    id = Column(String(36), primary_key=True,
                default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a Base instance
        """
        s_class = str(self.__class__.__name__)
        if DATA.get(s_class) is None:
            DATA[s_class] = {}

        self.id = kwargs.get('id', str(uuid.uuid4()))
        if kwargs.get('created_at') is not None:
            self.created_at = datetime.strptime(kwargs.get('created_at'),
                                                TIMESTAMP_FORMAT)
        else:
            self.created_at = datetime.utcnow()
        if kwargs.get('updated_at') is not None:
            self.updated_at = datetime.strptime(kwargs.get('updated_at'),
                                                TIMESTAMP_FORMAT)
        else:
            self.updated_at = datetime.utcnow()

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """ Equality
        """
        if type(self) != type(other):
            return False
        if not isinstance(self, Base):
            return False
        return (self.id == other.id)

    def to_json(self, for_serialization: bool = False) -> dict:
        """ Convert the object a JSON dictionary
        """
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key[0] == '_':
                continue
            if type(value).__name__ == 'InstanceState':  # Filter out InstanceState
                continue
            if type(value) is datetime:
                result[key] = value.strftime(TIMESTAMP_FORMAT)
            else:
                result[key] = value
        return result

    @classmethod
    def load_from_file(cls):
        """ Load all objects from file """
        s_class = cls.__name__
        file_path = ".db_{}.json".format(s_class)

        # Debugging: print class name and file path
        print(f"[DEBUG] Class Name: {s_class}")
        print(f"[DEBUG] File Path: {file_path}")

        DATA[s_class] = {}

        if not path.exists(file_path):
            # Debugging: print if the file does not exist
            print(f"[DEBUG] File does not exist: {file_path}")
            return

        # Debugging: print if the file exists and is being opened
        print(f"[DEBUG] File exists, opening: {file_path}")

        with open(file_path, 'r') as f:
            objs_json = json.load(f)

            # Debugging: print the loaded JSON data
            print(f"[DEBUG] Loaded JSON data: {objs_json}")

            for obj_id, obj_json in objs_json.items():
                # Debugging: print each object ID and corresponding JSON data
                print(f"[DEBUG] Object ID: {obj_id}, Object Data: {obj_json}")
                print(f"[DEBUG] Creating instance of {s_class}")
                DATA[s_class][obj_id] = cls(**obj_json)

                # Debugging: print confirmation of object creation
                print(
                    f"[DEBUG] Created instance of {s_class} with ID: {obj_id}")

    @classmethod
    def save_to_file(cls):
        """ Save all objects to file
        """
        s_class = cls.__name__
        file_path = ".db_{}.json".format(s_class)
        objs_json = {}
        for obj_id, obj in DATA[s_class].items():
            objs_json[obj_id] = obj.to_json(True)

        with open(file_path, 'w') as f:
            json.dump(objs_json, f)

    def save_to_db(self):
        print("[DEBUG] Saving to DB")
        session = SessionLocal()
        try:
            print("[DEBUG] Adding to session")
            session.add(self)
            print("[DEBUG] Commiting session")
            session.commit()
            user_id = self.id
            print(f"User ID: {user_id}")
        except Exception as e:
            print("[DEBUG] Error occurred while saving to DB:", e)
            print("[DEBUG] Rolling back session")
            session.rollback()
            raise
        finally:
            print("[DEBUG] Closing session")
            session.close()

    def save(self):
        """ Save current object
        """
        try:
            """s_class = self.__class__.__name__"""
            self.updated_at = datetime.utcnow()
            """DATA[s_class][self.id] = self
            self.__class__.save_to_file()"""
            self.save_to_db()
        except Exception as e:
            print("[DEBUG] Error occurred while saving:", e)

    def remove(self):
        """Remove the object from the database"""
        session = SessionLocal()
        try:
            session.delete(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def remove_from_file(self):
        """ Remove object
        """
        s_class = self.__class__.__name__
        if DATA[s_class].get(self.id) is not None:
            del DATA[s_class][self.id]
            self.__class__.save_to_file()
            self.remove_from_db()

    @classmethod
    def count_file(cls) -> int:
        """ Count all objects
        """
        s_class = cls.__name__
        return len(DATA[s_class].keys())

    @classmethod
    def count(cls) -> int:
        """Count all objects in the corresponding table."""
        session = SessionLocal()
        try:
            # Perform a COUNT(*) query on the class's table
            count_result = session.query(
                func.count()).select_from(cls).scalar()
        finally:
            session.close()

        return count_result

    @classmethod
    def all_from_db(cls):
        """Retrieve all objects"""
        session = SessionLocal()
        try:
            return session.query(cls).all()
        finally:
            session.close()

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """ Return all objects
        """
        return cls.search()

    @classmethod
    def get_from_db(cls, object_id: str):
        """Retrieve an object by its ID from the database"""
        session = SessionLocal()
        try:
            return session.query(cls).filter_by(id=object_id).first()
        finally:
            session.close()

    @classmethod
    def get(cls, id: str) -> TypeVar('Base'):
        """ Return one object by ID
        """
        s_class = cls.__name__
        return DATA[s_class].get(id)

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """Search for objects in the database based on the provided attributes.

        Args:
            attributes (dict): Key-value pairs indicating the attributes to search for.

        Returns:
            List[Base]: A list of objects matching the provided attributes.
        """

        # Get the name of the class
        s_class = cls.__name__

        # Define an inner function to perform the search
        def _search(obj):
            """Check if the object matches the provided attributes.

            Args:
                obj (Base): The object to check.

            Returns:
                bool: True if the object matches all the attributes, False otherwise.
            """
            # If no attributes are provided, return True
            if len(attributes) == 0:
                return True

            # Check if the object matches all the attributes
            for k, v in attributes.items():
                if (getattr(obj, k) != v):
                    return False
            return True

        # Filter the objects based on the search function and return the results
        return list(filter(_search, DATA[s_class].values()))

    @classmethod
    def search_db(cls, attributes: dict = {}):
        """Search for objects in the MySQL database based on provided attributes."""
        session = SessionLocal()
        try:
            # Start building the query from the class
            query = session.query(cls)

            # Check if we're querying the User class, then use eager loading for logs
            if cls.__name__ == 'User':
                query = query.options(joinedload(cls.logs))

            # If attributes are provided, dynamically build the WHERE clause
            if attributes:
                # Dynamically create filters based on attributes
                filters = [getattr(cls, k) == v for k, v in attributes.items()]
                query = query.filter(and_(*filters))

            # Execute the query and return the results as class instances
            results = query.all()

        except Exception as e:
            session.rollback()  # Rollback in case of an error
            raise e  # Re-raise the exception for further handling/logging

        finally:
            session.close()  # Ensure the session is closed no matter what

        return results
