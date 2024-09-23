#!/usr/bin/python3
"""Test BaseClass for expected behavior and documentation"""
from datetime import datetime
import pycodestyle
import unittest
import models
import json
import inspect

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models.base import BaseClass, DATA
# BaseClass = models.base.Base

my_db_name = "adonis_db"
DATABASE_URL_WITH_DB = f"mysql://root:56213@localhost/{my_db_name}"
engine_with_db = create_engine(DATABASE_URL_WITH_DB, echo=False)
SessionLocal = sessionmaker(bind=engine_with_db)

class TestBaseClass(unittest.TestCase):

    def setUp(self):
        self.session = SessionLocal()
        self.now = datetime.now()
        self.base_model = BaseClass(id=1, created_at=self.now, updated_at=self.now)

    def tearDown(self):
        self.session.close()

    def test_init_creates_instance(self):
        instance = BaseClass()
        self.assertIsInstance(instance, BaseClass)
        self.assertIsNotNone(instance.id)
        self.assertIsInstance(instance.created_at, datetime)
        self.assertIsInstance(instance.updated_at, datetime)

    def test_to_json(self):
        instance = BaseClass()
        json_data = instance.to_json()
        self.assertIn('id', json_data)
        self.assertIn('created_at', json_data)
        self.assertIn('updated_at', json_data)

    def test_str(self):
        expected_str = f"BaseClass(id=1, created_at={self.now}, updated_at={self.now})"
        self.assertEqual(str(self.base_model), expected_str)

    def test_save_to_db(self):
        instance = BaseClass()
        instance.save_to_db()
        
        retrieved_instance = self.session.query(BaseClass).filter_by(id=instance.id).first()
        self.assertIsNotNone(retrieved_instance)

    def test_remove_from_db(self):
        instance = BaseClass()
        instance.save_to_db()
        instance.remove()
        
        retrieved_instance = self.session.query(BaseClass).filter_by(id=instance.id).first()
        self.assertIsNone(retrieved_instance)

    def test_count(self):
        initial_count = BaseClass.count()
        instance1 = BaseClass()
        instance1.save_to_db()
        instance2 = BaseClass()
        instance2.save_to_db()

        self.assertEqual(BaseClass.count(), initial_count + 2)

    def test_load_from_file(self):
        BaseClass.load_from_file()
        count_after_load = BaseClass.count()
        self.assertGreater(count_after_load, 0)

    def test_search(self):
        instance1 = BaseClass()
        instance1.save_to_db()
        instance2 = BaseClass()
        instance2.save_to_db()

        results = BaseClass.search({})
        self.assertEqual(len(results), 2)

    def test_remove_from_file(self):
        instance = BaseClass()
        instance.save_to_db()
        instance.remove_from_file()
        
        self.assertIsNone(BaseClass.get(instance.id))
    
    def test_pep8_conformance(self):
        """Test that models/base.py conforms to PEP8."""
        for path in ['models/base.py',
                     'tests/test_models/test_base.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

if __name__ == '__main__':
    unittest.main()

# TypeError: strptime() argument 1 must be str, not datetime.datetime

# PROPOSED CHANGES TO BaseClass

# class BaseClass():
#     """Base class that other models will inherit from"""
#     __abstract__ = True

#     id = Column(String(36), primary_key=True,
#                 default=lambda: str(uuid.uuid4()))
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     def __init__(self, *args: list, **kwargs: dict):
#         """ Initialize a Base instance """
#         s_class = str(self.__class__.__name__)
#         if DATA.get(s_class) is None:
#             DATA[s_class] = {}

#         self.id = kwargs.get('id', str(uuid.uuid4()))

#         # Check type before parsing
#         created_at = kwargs.get('created_at')
#         if isinstance(created_at, str):
#             self.created_at = datetime.strptime(created_at, TIMESTAMP_FORMAT)
#         elif isinstance(created_at, datetime):
#             self.created_at = created_at
#         else:
#             self.created_at = datetime.utcnow()

#         updated_at = kwargs.get('updated_at')
#         if isinstance(updated_at, str):
#             self.updated_at = datetime.strptime(updated_at, TIMESTAMP_FORMAT)
#         elif isinstance(updated_at, datetime):
#             self.updated_at = updated_at
#         else:
#             self.updated_at = datetime.utcnow()
