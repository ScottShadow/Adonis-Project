#!/usr/bin/python3
"""Test BaseClass for expected behavior and documentation"""
from datetime import datetime
import inspect
import models
import pycodestyle
import time
import unittest
import json
from unittest.mock import mock, mock_open, MagicMock
from models.base import Base, DATA
BaseClass = models.base.BaseClass
module_doc = models.base.__doc__


class TestBaseClassDocs(unittest.TestCase):
    """Tests to check the documentation and style of BaseClass class"""

    @classmethod
    def setUpClass(self):
        """Set up for docstring tests"""
        self.base_funcs = inspect.getmembers(BaseClass, inspect.isfunction)

    def setUp(self):
        """Set up initial conditions before each docstring test"""
        self.cls = Base
        self.s_class = self.cls.__name__
        self.file_path = f".db_{self.s_class}.json"
        DATA[self.s_class] = {}

    def test_pep8_conformance(self):
        """Test that models/base.py conforms to PEP8."""
        for path in ['models/base.py',
                     'tests/test_models/test_base.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(module_doc, None,
                         "base.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "base.py needs a docstring")

    def test_class_docstring(self):
        """Test for the BaseClass class docstring"""
        self.assertIsNot(BaseClass.__doc__, None,
                         "BaseClass class needs a docstring")
        self.assertTrue(len(BaseClass.__doc__) >= 1,
                        "BaseClass class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in BaseClass methods"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertIsNot(
                    func[1].__doc__,
                    None,
                    "{:s} method needs a docstring".format(func[0])
                )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class TestBaseClass(unittest.TestCase):
    """Test the BaseClass class"""
    def test_instantiation(self):
        """Test that object is correctly created"""
        inst = BaseClass()
        self.assertIs(type(inst), BaseClass)
        inst.name = "Adonis"
        inst.number = 21
        attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "number": int
        }
        for attr, typ in attrs_types.items():
            with self.subTest(attr=attr, typ=typ):
                self.assertIn(attr, inst.__dict__)
                self.assertIs(type(inst.__dict__[attr]), typ)
        self.assertEqual(inst.name, "Adonis")
        self.assertEqual(inst.number, 21)

    def test_datetime_attributes(self):
        """Test that two BaseClass instances have different datetime objects
        and that upon creation have identical updated_at and created_at
        value."""
        tic = datetime.now()
        inst1 = BaseClass()
        toc = datetime.now()
        self.assertTrue(tic <= inst1.created_at <= toc)
        time.sleep(1e-4)
        tic = datetime.now()
        inst2 = BaseClass()
        toc = datetime.now()
        self.assertTrue(tic <= inst2.created_at <= toc)
        self.assertEqual(inst1.created_at, inst1.updated_at)
        self.assertEqual(inst2.created_at, inst2.updated_at)
        self.assertNotEqual(inst1.created_at, inst2.created_at)
        self.assertNotEqual(inst1.updated_at, inst2.updated_at)

    def test_uuid(self):
        """Test that id is a valid uuid"""
        inst1 = BaseClass()
        inst2 = BaseClass()
        for inst in [inst1, inst2]:
            uuid = inst.id
            with self.subTest(uuid=uuid):
                self.assertIs(type(uuid), str)
                self.assertRegex(uuid,
                                 '^[0-9a-f]{8}-[0-9a-f]{4}'
                                 '-[0-9a-f]{4}-[0-9a-f]{4}'
                                 '-[0-9a-f]{12}$')
        self.assertNotEqual(inst1.id, inst2.id)

    def test_to_json(self):
        """Test conversion of object attributes to dictionary for json"""
        my_model = BaseClass()
        my_model.name = "Adonis"
        my_model.my_number = 21
        d = my_model.to_json()
        expected_attrs = ["id",
                          "created_at",
                          "updated_at",
                          "name",
                          "my_number",
                          "__class__"]
        self.assertCountEqual(d.keys(), expected_attrs)
        self.assertEqual(d['__class__'], 'BaseClass')
        self.assertEqual(d['name'], "Adonis")
        self.assertEqual(d['my_number'], 21)

    def test_to_json_values(self):
        """test that values in dict returned from to_json are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        bm = BaseClass()
        new_d = bm.to_json()
        self.assertEqual(new_d["__class__"], "BaseClass")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], bm.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], bm.updated_at.strftime(t_format))

    

    @mock.patch('models.storage')
    def test_save(self, mock_storage):
        """Test that save method updates `updated_at` and calls
        `storage.save`"""
        inst = BaseClass()
        old_created_at = inst.created_at
        old_updated_at = inst.updated_at
        inst.save()
        new_created_at = inst.created_at
        new_updated_at = inst.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)
        self.assertTrue(mock_storage.new.called)
        self.assertTrue(mock_storage.save.called)

    @mock.patch("BaseClass.os.path.exists")
    @mock.patch("BaseClass.open", new_callable=mock_open, read_data='{"1": {"id": "1", "name": "test"}}')
    def test_load_from_file_exists(self, mock_open, mock_path_exists):
        mock_path_exists.return_value = True

        self.cls.load_from_file()

        mock_open.assert_called_once_with(self.file_path, 'r')
        self.assertIn("1", DATA[self.s_class])

    @mock.patch("BaseClass.os.path.exists")
    def test_load_from_file_not_exists(self, mock_path_exists):
        mock_path_exists.return_value = False

        self.cls.load_from_file()

        self.assertNotIn("1", DATA[self.s_class])

    @mock.patch("BaseClass.open", new_callable=mock_open)
    def test_save_to_file(self, mock_open):
        obj = MagicMock()
        obj.to_json.return_value = {"id": "1", "name": "test"}
        DATA[self.s_class]["1"] = obj

        self.cls.save_to_file()

        mock_open.assert_called_once_with(self.file_path, 'w')
        mock_open().write.assert_called_once_with(json.dumps({"1": {"id": "1", "name": "test"}}))

    @mock.patch("BaseClass.SessionLocal")
    def test_save_to_db(self, mock_session_local):
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session

        obj = Base()
        obj.id = "1"
        obj.save_to_db()

        mock_session.add.assert_called_once_with(obj)
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()

    @mock.patch.object(Base, 'save_to_file')
    @mock.patch.object(Base, 'save_to_db')
    def test_save(self, mock_save_to_db, mock_save_to_file):
        obj = Base()
        obj.id = "1"
        obj.save()

        mock_save_to_file.assert_called_once()
        mock_save_to_db.assert_called_once()

    @mock.patch("BaseClass.SessionLocal")
    def test_remove(self, mock_session_local):
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session

        obj = Base()
        obj.remove()

        mock_session.delete.assert_called_once_with(obj)
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()

    @mock.patch.object(Base, 'save_to_file')
    @mock.patch.object(Base, 'remove')
    def test_remove_from_file(self, mock_remove, mock_save_to_file):
        obj = Base()
        obj.id = "1"
        DATA[self.s_class]["1"] = obj

        obj.remove_from_file()

        mock_save_to_file.assert_called_once()
        mock_remove.assert_called_once()
        self.assertNotIn("1", DATA[self.s_class])

    def test_count_file(self):
        DATA[self.s_class]["1"] = Base()
        self.assertEqual(self.cls.count_file(), 1)

    @mock.patch("BaseClass.SessionLocal")
    def test_count(self, mock_session_local):
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_session.query().select_from().scalar.return_value = 1

        count = self.cls.count()
        self.assertEqual(count, 1)
        mock_session.close.assert_called_once()

    @mock.patch("BaseClass.SessionLocal")
    def test_all_from_db(self, mock_session_local):
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_session.query().all.return_value = ["obj1", "obj2"]

        result = self.cls.all_from_db()
        self.assertEqual(result, ["obj1", "obj2"])
        mock_session.close.assert_called_once()

    @mock.patch.object(Base, 'search')
    def test_all(self, mock_search):
        mock_search.return_value = ["obj1", "obj2"]
        result = self.cls.all()
        self.assertEqual(result, ["obj1", "obj2"])
        mock_search.assert_called_once()

    @mock.patch("BaseClass.SessionLocal")
    def test_get_from_db(self, mock_session_local):
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_session.query().filter_by().first.return_value = "obj"

        result = self.cls.get_from_db("1")
        self.assertEqual(result, "obj")
        mock_session.close.assert_called_once()

    def test_get(self):
        obj = Base()
        obj.id = "1"
        DATA[self.s_class]["1"] = obj

        result = self.cls.get("1")
        self.assertEqual(result, obj)

    def test_search(self):
        obj = Base()
        obj.id = "1"
        obj.name = "test"
        DATA[self.s_class]["1"] = obj

        result = self.cls.search({"name": "test"})
        self.assertEqual(result, [obj])

        result_empty = self.cls.search({"name": "nonexistent"})
        self.assertEqual(result_empty, [])

    @mock.patch("BaseClass.SessionLocal")
    def test_search_db(self, mock_session_local):
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_session.query().filter().all.return_value = ["obj1", "obj2"]

        result = self.cls.search_db({"name": "test"})
        self.assertEqual(result, ["obj1", "obj2"])
        mock_session.close.assert_called_once()
