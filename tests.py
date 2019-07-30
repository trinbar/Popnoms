from unittest import TestCase
from server import app
from test_model import *


class FlaskTests(TestCase):
    """Tests for Popnoms site."""

    def setUp(self):
        """Run this code before each test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        """Tests rendering of homepage."""

        result = self.client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Hola', result.data)

    def test_resgistration(self):
        """Tests registration_form route."""

        result = self.client.get('/registration_form')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Name', result.data)
        self.assertIn('Email', result.data)


class DatabaseFlaskTests(TestCase):
    """Tests eb_helper and mb_helper functions."""

    def setUp(self):
        """Tests for database."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to the test db
        connect_to_db(app, 'postgresql:///testdb')

        # Create tables and add sample data
        db.create_all()
        example_data()


    def tearDown(self):
        """Tears the database down after each test is called."""

        db.session.close()
        db.drop_all()


     def test_login(self):
        """Tests login with example data."""

        result = self.client.post('/login_form', 
            data={'user_id': '1', 
            'username': 'trinbar', 
            'password': 'password', 
            'email': 'dunbar.trinity@gmail.com', 
            'location': 'San Francisco, CA, USA'}, 
            follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Search", result.data)

    def test_login_fail(self):
        """Checks login fail with invalid data"""

        result = self.client.post("/login_form", 
            data={'user_id': '3',
            'username': 'invalid'
            'password': ''
            'email': 'invalid@gmail.com',
            'location': 'invalid'}, 
            follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("User Login", result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()