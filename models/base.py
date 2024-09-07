#!/usr/bin/env python3
""" Base module with mysql database
"""
from datetime import datetime
from typing import TypeVar, List, Iterable
from os import path
import json
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, func
from sqlalchemy.exc import ProgrammingError

# Database configuration (without specifying the database name)
DATABASE_URL = "mysql://root:56213@localhost/"

# Database name
my_db_name = "adonis_db"

# Create an engine for MySQL without specifying a database
engine = create_engine(DATABASE_URL)

# Function to create the database if it doesn't exist


def create_database(current_engine, db_name):
    conn = current_engine.connect()
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
create_database(engine, my_db_name)

# Once the database exists, you can create an engine bound to that database
DATABASE_URL_WITH_DB = f"mysql://root:56213@localhost/{my_db_name}"
engine_with_db = create_engine(DATABASE_URL_WITH_DB, echo=True)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_with_db)

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
        s_class = self.__class__.__name__
        self.updated_at = datetime.utcnow()
        DATA[s_class][self.id] = self
        self.__class__.save_to_file()
        self.save_to_db()

    def remove_from_db(self):
        """Remove the object from the database"""
        session = SessionLocal()
        try:
            session.delete(self)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def remove(self):
        """ Remove object
        """
        s_class = self.__class__.__name__
        if DATA[s_class].get(self.id) is not None:
            del DATA[s_class][self.id]
            self.__class__.save_to_file()
            self.remove_from_db()

    @classmethod
    def count(cls) -> int:
        """ Count all objects
        """
        s_class = cls.__name__
        return len(DATA[s_class].keys())

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
