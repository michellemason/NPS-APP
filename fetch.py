import os
from models import connect_db, db, User, Park, FavoritePark
from secret import API_SECRET_KEY
from app import app
import requests

API_BASE_URL = 'https://developer.nps.gov/api/v1/'

def fill_all_parks():
    """fill parks table with parks data"""

    response = requests.get(f"{API_BASE_URL}parks?limit=500&api_key={API_SECRET_KEY}")

    res_json = response.json()
    results = res_json['data']

    for result in results:
        add_park = Park(name=result['fullName'], code=result['parkCode'], states=result['states'])
        db.session.add(add_park)

    db.session.commit()

    return "Parks table filled"

def execute_all():
    db.drop_all()
    db.create_all()
    fill_all_parks()

execute_all()

# def add_park_from_api(park):
#     """Add park to favorites list in DB"""
#     id = park.get('id', None)
#     name = park.get('fullName', None)
#     code = park.get('parkCode', None)
#     states = park.get('states', None)

#     favorite = Park(id=id, name=name, code=code, states=states)
#     try:
#         db.session.add(favorite)
#         db.session.commit()

#     except Exception:
#         db.session.rollback()
#         print("Exception", str(Exception))
#         return "Sorry, please try again later", str(Exception)
#     return favorite