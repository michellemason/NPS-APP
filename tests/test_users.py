import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User
from app import app

os.environ['DATABASE_URL'] = "postgresql:///NPS_db"

db.create_all()

class UserModelTests(TestCase):
    """Tests for user model"""
    def setUp(self):
        """Add sample data and test user"""
        db.drop_all()
        db.create_all()

        u1 = User.register("test1", "password", "test1@email.com")
        u1id = 9999
        u1.id = u1id

        db.session.commit()

        u1 = User.query.get(u1id)

        self.u1 = u1
        self.u1id = u1id

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user(self):
        """Testing the user model"""
        u = User(username="test", password="password", email="test@email.com")
        db.session.add(u)
        db.session.commit()

        self.assertEqual(User.query.get(1), u)
        self.assertEqual(len(u.favorites), 0)

    def test_register(self):
        u = User.register('test', 'test@email.com', 'password')
        uid = 9998
        u.id = uid
        db.session.commit()

        u = User.query.get(uid)
        self.assertIsNotNone(u)
        self.assertEqual(u.username, "test")
        self.assertNotEqual(u.password, 'password')
        self.assertTrue(u.password.startswith("$2b$"))

    def test_authenticate(self):
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.u1id)

    def test_invalid_username(self):
        self.assertFalse(User.authenticate("wrong_user", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "wrong_password"))