import requests
import os
from unittest import TestCase
from models import db, Park
from app import app 
from secret import API_SECRET_KEY

os.environ['DATABASE_URL'] = "postgresql:///NPS_db"

db.create_all()

API_BASE_URL = 'https://developer.nps.gov/api/v1/'

class APIRequestTests(TestCase):
    """Tests for external API requests"""
    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_request_parkCode(self):
        """Test for getting parkcode"""
        response = requests.get(f'{API_BASE_URL}parks?api_key={API_SECRET_KEY}')
        res_json = response.json()
        results = res_json['data']

        self.assertIsNotNone(results)
        self.assertEqual(results[0]['parkCode'], 'abli')

    def test_request_fullName(self):
        """Test for getting full park name"""
        response = requests.get(f'{API_BASE_URL}parks?api_key={API_SECRET_KEY}')
        res_json = response.json()
        results = res_json['data']

        self.assertIsNotNone(results)
        self.assertEqual(results[0]['fullName'], 'Abraham Lincoln Birthplace National Historical Park')

    def test_request_description(self):
        """Test for getting park description"""
        response = requests.get(f'{API_BASE_URL}parks?api_key={API_SECRET_KEY}')
        res_json = response.json()
        results = res_json['data']

        self.assertIsNotNone(results)
        self.assertEqual(results[0]['description'], "For over a century people from around the world have come to rural Central Kentucky to honor the humble beginnings of our 16th president, Abraham Lincoln. His early life on Kentucky's frontier shaped his character and prepared him to lead the nation through Civil War. The country's first memorial to Lincoln, built with donations from young and old, enshrines the symbolic birthplace cabin.")


    