#!/usr/bin/python3
"""
Test Log for expected behavior and documentation
python -m unittest tests/test_models/test_log.py
"""
import unittest
from sqlalchemy.orm import sessionmaker
from models.log import Log
from models.user import User
from models.base import SessionLocal
import uuid

class TestLog(unittest.TestCase):

    def setUp(self):
        """ Create a user for testing"""
        self.session = SessionLocal()
        
        unique_suffix = str(uuid.uuid4())
        self.test_user = User(id=str(uuid.uuid4()),
                              username=f"test_user_{unique_suffix}",
                              email=f"test_{unique_suffix}@example.com",
                              password="12345678",
                              total_xp=0)
        self.session.add(self.test_user)
        self.session.commit()

    def tearDown(self):
        """ Clean up the database after tests """
        self.session.query(Log).filter_by(user_id=self.test_user.id).delete()
        self.session.query(User).filter_by(id=self.test_user.id).delete()
        self.session.commit()
        self.session.close()  

    def test_log_creation(self):
        log = Log(
            user_id=self.test_user.id,
            habit_type="Exercise",
            habit_name="Morning Run"
        )
        self.session.add(log)
        self.session.commit()
        
        retrieved_log = self.session.query(Log).filter_by(id=log.id).first()
        self.assertIsNotNone(retrieved_log)
        self.assertEqual(retrieved_log.habit_name, "Morning Run")
        self.assertEqual(retrieved_log.user_id, self.test_user.id)

    def test_update_user_xp(self):
        log = Log(
            user_id=self.test_user.id,
            habit_type="Exercise",
            habit_name="Morning Run",
            xp=10
        )
        log.update_user_xp()
        
        updated_user = self.session.query(User).get(self.test_user.id)
        self.assertEqual(updated_user.total_xp, 10)

    def test_required_fields(self):
        with self.assertRaises(ValueError):
            Log(user_id=None, habit_type="Exercise", habit_name="Morning Run")
        
        with self.assertRaises(ValueError):
            Log(user_id=self.test_user.id, habit_type=None, habit_name="Morning Run")

if __name__ == '__main__':
    unittest.main()

# FAIL: test_update_user_xp (tests.test_models.test_log.TestLog.test_update_user_xp)
# ----------------------------------------------------------------------
# Traceback (most recent call last):
#   File "C:\Users\Kamikazi\Projects\Adonis-Project\tests\test_models\test_log.py", line 58, 
# in test_update_user_xp
#     self.assertEqual(updated_user.total_xp, 10)
# AssertionError: 0 != 10