#!/usr/bin/python3
"""
Contains the TestTagDocs classes
"""
import inspect
import models
from models import tag
from models.base import Tag
import pycodestyle
import unittest
Tag = tag.Tag
module_doc = models.tag.__doc__

class TesttagDocs(unittest.TestCase):
    """Tests to check the documentation and style of Tag class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the docstring tests"""
        cls.tag_f = inspect.getmembers(Tag, inspect.isfunction)

    def test_pycodestyle_conformance_tag(self):
        """Test that models/tag.py conforms to pycodestyle."""
        pycodestyles = pycodestyle.StyleGuide(quiet=True)
        result = pycodestyles.check_files(['models/tag.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_tag(self):
        """Test that testing/test_models/test_tag.py conforms to pycodestyle."""
        pycodestyles = pycodestyle.StyleGuide(quiet=True)
        result = pycodestyles.check_files(['tests/test_models/test_tag.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_tag_module_docstring(self):
        """Test for the tag.py module docstring"""
        self.assertIsNot(tag.__doc__, None,
                         "tag.py needs a docstring")
        self.assertTrue(len(tag.__doc__) >= 1,
                        "tag.py needs a docstring")

    def test_tag_class_docstring(self):
        """Test for the tag class docstring"""
        self.assertIsNot(tag.__doc__, None,
                         "tag class needs a docstring")
        self.assertTrue(len(tag.__doc__) >= 1,
                        "tag class needs a docstring")

    def test_tag_func_docstrings(self):
        """Test for the presence of docstrings in tag methods"""
        for func in self.tag_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

class TestTag(unittest.TestCase):
    """Test the Tag class"""
    def test_instantiation(self):
        """Test that object is correctly created"""
        inst = Tag()
        self.assertIs(type(inst), Tag)
        inst.name = "Scholar"
        inst.number = 22
        attrs_types = {
            "id": str,
            "name": str,
            "category": str, 
            "description": str,
            
            description = Column(String(500), nullable=True)
            level = Column(Integer, nullable=True)

        }
        for attr, typ in attrs_types.items():
            with self.subTest(attr=attr, typ=typ):
                self.assertIn(attr, inst.__dict__)
                self.assertIs(type(inst.__dict__[attr]), typ)
        self.assertEqual(inst.name, "Holberton")
        self.assertEqual(inst.number, 89)
