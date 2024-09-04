#!/usr/bin/env python3
""" Base module
"""
from datetime import datetime
from typing import TypeVar, List, Iterable
from os import path
import json
import uuid
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA = {}


class BaseClass():
    """ Base class
    """

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
                obj_instance = cls(**obj_json)
                DATA[s_class][obj_id] = cls(**obj_json)

                # Debugging: print confirmation of object creation
                print(f"[DEBUG] Loaded object {obj_id} with properties:")
                for key, value in obj_instance.__dict__.items():
                    print(f"    {key}: {value}")

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

    def save(self):
        """ Save current object
        """
        s_class = self.__class__.__name__
        self.updated_at = datetime.utcnow()
        DATA[s_class][self.id] = self
        self.__class__.save_to_file()

    def remove(self):
        """ Remove object
        """
        s_class = self.__class__.__name__
        if DATA[s_class].get(self.id) is not None:
            del DATA[s_class][self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """ Count all objects
        """
        s_class = cls.__name__
        return len(DATA[s_class].keys())

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """ Return all objects
        """
        return cls.search()

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
        print(f"FOUND \n\n {list(filter(_search, DATA[s_class].values()))}")
        # Filter the objects based on the search function and return the results
        return list(filter(_search, DATA[s_class].values()))
