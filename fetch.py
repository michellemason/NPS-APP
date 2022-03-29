import os
from textwrap import fill
from models import connect_db, db, User, Park, FavoritePark
from secret import API_SECRET_KEY
# from app import app
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

def add_park_from_api(park):
    """Add park to favorites list in DB"""
    id = park.get('id', None)
    name = park.get('fullName', None)
    code = park.get('parkCode', None)
    states = park.get('states', None)

    favorite = Park(id=id, name=name, code=code, states=states)
    try:
        db.session.add(favorite)
        db.session.commit()

    except Exception:
        db.session.rollback()
        print("Exception", str(Exception))
        return "Sorry, please try again later", str(Exception)
    return favorite

def execute_all():
    db.drop_all()
    db.create_all()
    fill_all_parks()


    execute_all()







# def all_parks():
#     """fill parks table with parks data"""

#     response = requests.get(f"{API_BASE_URL}parks?limit=500&api_key={API_SECRET_KEY}")

#     res_json = response.json()
#     results = res_json['data']
    
#     for result in results:
#         add_park = Park(name=result['fullName'], code=result['parkCode'])
#         db.session.add(add_park)
    
#     db.session.commit()

#     return "Parks table filled"

# def all_activities():
#     """Fill activities table with data"""

#     response = requests.get(f"{API_BASE_URL}activities/parks?limit=500&api_key={API_SECRET_KEY}")

#     res_json = response.json()
#     results = res_json['data']

#     for result in results:
#         add_activity = Activity(act_api_id=result['id'], name=result['name'])
#         db.session.add(add_activity)
    
#     db.session.commit()

#     return "Activities table filled"

# def all_states():
#     """Fill states table with data"""

#     response = requests.get(f"{API_BASE_URL}parks?limit=500&api_key={API_SECRET_KEY}")

#     res_json = response.json()
#     results = res_json['data']
    
#     for result in results:
#         id = result['states']
#         add_state = State.no_duplicates(id=id)
#         db.session.add(add_state)
    
#     db.session.commit()

#     return "States table filled"

# def parks_activities():
#     """Fill parks_activities table"""

#     response = requests.get(f"{API_BASE_URL}activities/parks?limit=500&api_key={API_SECRET_KEY}")

#     res_json = response.json()
#     results = res_json['data']

#     for result in results:
#         for code in result['parks']:
#             # park_id = code['parkCode']
#             act_id = result['id']
#             name = result['name']
#             # if (park_id != 'mall') and (park_id != 'ston'):
#                 #handles strange codes in API data not in park data
#             add_result = ParkActivity(activity_id=act_id, activity_name=name)
#             db.session.add(add_result)
    
#     db.session.commit()
#     return "Parks_Activities Table Filled"

# def parks_states():
#     """Fill parks_states table"""

#     response = requests.get(f"{API_BASE_URL}parks?limit=500&api_key={API_SECRET_KEY}")

#     res_json = response.json()
#     results = res_json['data']

#     for result in results:
#         # park_id = result['id']
#         state_id = result['states']
#         # if (park_id != '77E0D7F0-1942-494A-ACE2-9004D2BDC59E') and (park_id != '6DA17C86-088E-4B4D-B862-7C1BD5CF236B') and (park_id != 'E4C7784E-66A0-4D44-87D0-3E072F5FEF43'):
#         add_result = ParkState(state_id=state_id)
#         db.session.add(add_result)

#     db.session.commit()
#     return "Parks_States table filled"

