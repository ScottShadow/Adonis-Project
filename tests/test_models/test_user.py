#!/usr/bin/python3
"""
Test User for expected behavior and documentation
python -m unittest tests/test_models/test_user.py
"""
import unittest
from models.user import User  
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
import uuid

class TestUserModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the database for tests."""
        cls.engine = create_engine('sqlite:///:memory:')  # Use an in-memory SQLite database for testing
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        """Set up a new session and a user for each test."""
        unique_suffix = str(uuid.uuid4())
        self.session = self.Session()
        self.test_user = User(
            id=str(uuid.uuid4()),
            username=f"test_user_{unique_suffix}",
            email=f"test_{unique_suffix}@example.com",
            password='password123',  # Will be hashed
            first_name='Test',
            last_name='User',
            age=30,
            skills='Python, SQL'
        )
        self.session.add(self.test_user)
        self.session.commit()
        

    def tearDown(self):
        """Rollback any changes made during tests."""
        self.session.rollback()
        self.session.close()

    def test_user_initialization(self):
        """Test user initialization."""

        self.assertEqual(self.test_user.email, 'test@example.com')
        self.assertEqual(self.test_user.username, 'testuser')
        self.assertTrue(self.test_user.password is not None)
        self.assertEqual(self.test_user.first_name, 'Test')
        self.assertEqual(self.test_user.last_name, 'User')
        self.assertEqual(self.test_user.age, 30)
        self.assertEqual(self.test_user.skills, 'Python, SQL')

    def test_password_hashing(self):
        """Test password hashing and validation."""

        self.assertTrue(self.test_user.is_valid_password('password123'))
        self.assertFalse(self.test_user.is_valid_password('wrongpassword'))

    def test_display_name(self):
        """Test the display name generation."""

        self.assertEqual(self.test_user.display_name(), 'Test User')
        self.test_user.first_name = ''
        self.assertEqual(self.test_user.display_name(), 'User')
        self.test_user.last_name = ''
        self.assertEqual(self.test_user.display_name(), 'test@example.com')

    def test_to_json(self):
        """Test JSON serialization."""
        json_data = self.test_user.to_json()
        self.assertIn('email', json_data)
        self.assertIn('username', json_data)
        self.assertIn('total_xp', json_data)  # Ensure total_xp is included

    def test_level_calculation(self):
        """Test level calculation based on XP."""
        self.assertEqual(self.test_user.level, 0)  # Starting level should be 0
        self.test_user.total_xp = 5000  # Enough XP for level 10
        self.assertEqual(self.test_user.level, 10)

    def test_invalid_user_creation(self):
        """Test invalid user creation scenarios."""
        with self.assertRaises(ValueError):
            User(username='newuser', password='password123')  # Missing email
        with self.assertRaises(ValueError):
            User(email='newuser@example.com', password='password123')  # Missing username
        with self.assertRaises(ValueError):
            User(email='newuser@example.com', username='newuser')  # Missing password

    @classmethod
    def tearDownClass(cls):
        """Tear down the database after all tests."""
        Base.metadata.drop_all(cls.engine)

if __name__ == '__main__':
    unittest.main()
