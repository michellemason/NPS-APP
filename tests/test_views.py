import os
from unittest import TestCase
from models import db, User, Park, FavoritePark
from app import app

os.environ['DATABASE_URL'] = "postgresql:///NPS_db"

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserViewsTests(TestCase):
    def setUp(self):
        """Add sample data and test user"""
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        u1 = User.register('test', "password", 'test@email.com')
        u1id = 9997
        u1.id = u1id

        db.session.commit()

        u1 = User.query.get(u1id)

        self.u1 = u1
        self.u1id = u1id

        p1 = Park(name='TestPark', code='TTPP', states='AK')

        db.session.add(p1)
        p1id = 2222
        p1.id = p1id

        db.session.commit()

        self.p1 = p1
        self.p1id = p1id

    def tearDown(self):
        res = super().tearDown()
        db.session.delete(self.u1)
        db.session.commit()
        db.session.rollback()
        return res

    def test_guest_root(self):
        """Test base view for user not signed in."""
        with self.client as c:
            resp = c.get('/', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Browse Parks by State", str(resp.data))

    def test_state_pages(self):
        """Test state page for user not signed in."""
        with self.client as c:
            resp = c.get('/state/AK')

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Alaska", str(resp.data))

    def test_park_pages(self):
        """Test state page for user not signed in."""
        with self.client as c:
            resp = c.get('/state/AK/gaar')

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Gates of the Arctic", str(resp.data))

    def test_guest_signup_view(self):
        """Test sign up page view."""
        with self.client as c:
            resp = c.get('/register')

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Create An Account", str(resp.data))

    def test_new_user_register(self):
        """Test registering a new user."""
        with self.client as c:
            resp = c.post('/register', data={
                "email": "test2@email.com",
                "username": "tester",
                "password": "password"}, follow_redirects=True)

            user = User.query.filter_by(username="tester").one()

            self.assertIsNotNone(user)
            self.assertEqual(user.username, "tester")
            self.assertIn("Browse Parks by State", str(resp.data))

            db.session.delete(user)
            db.session.commit()

    def test_valid_login(self):
        """Test user login."""
        with self.client as c:
            resp = c.post('/login', data={
                "username": "test",
                "password": "password"
            }, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Hello, test!", str(resp.data))

    def test_invalid_login(self):
        """Test invalid login attempt."""
        with self.client as c:
            resp = c.post('/login', data={
                "username": "test",
                "password": "wrongpassword"
            }, follow_redirects=True)

        self.assertIn("Username/Password incorrect.", str(resp.data))

    def test_user_home_view(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess["CURR_USER_KEY"] = self.u1.id
            resp = c.get('/', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Bringing the parks to you", str(resp.data))