from audioop import add
from crypt import methods
from sqlite3 import IntegrityError
from fetch import fill_all_parks, add_park_from_api
from flask import Flask, render_template, g, redirect, session, request, flash, jsonify, make_response, url_for
from flask_wtf import FlaskForm
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Park, FavoritePark
from forms import CreateUserForm, LoginForm
from secret import API_SECRET_KEY
import os
import requests
import json

uri = os.environ.get("DATABASE_URL", "postgresql:///NPS_db")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

CURR_USER_KEY = "user_id"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "secret parks!")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

API_BASE_URL = 'https://developer.nps.gov/api/v1/'

connect_db(app)

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/')
def root():
    """Basic homepage reroute"""
    return redirect('/home')

@app.route('/home')
def homepage():
    """Actual omepage"""
    return render_template('home.html')


############# USER ROUTES #############

@app.route('/register', methods=["GET", "POST"])
def register_user():

    if CURR_USER_KEY in session:
        return redirect('/')

    form = CreateUserForm()
    if form.validate_on_submit():
        try:
            username = form.username.data
            password = form.password.data
            email = form.email.data
            new_user = User.register(username, password, email)
            db.session.commit()
        
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('register.html', form=form)

        do_login(new_user)
        flash("Account Created!", "success")
        return redirect('/') #need to create user pages
    
    return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """handle loging a user in"""
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            do_login(user)
            flash(f'Hello, {user.username}!', 'success')
            return redirect(f'/users/{user.id}')

        flash("Username/Password incorrect.", "danger")
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    do_logout()
    flash("See you next time!", 'success')
    return redirect('/')

@app.route('/users/<int:user_id>')
def users_page(user_id):
    """User profile"""

    user = User.query.get_or_404(user_id)
    ### ADD FAVORITES HERE LATER
    return render_template('users.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user"""
    if not g.user:
        flash("Unauthorized acces.", 'danger')
        return redirect('/')
    
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()
    session.pop(CURR_USER_KEY)
    flash(f"{g.user.username} has been deleted.", 'secondary')
    return redirect('/')

#### ADD EDIT AND DELETE USER ACTIONS

############### PARK ROUTES ###############

@app.route('/state/<state>')
def lookup_state(state):
    """Show a states parks"""
    response = requests.get(f'{API_BASE_URL}parks?api_key={API_SECRET_KEY}&stateCode={state}')

    res_json = response.json()
    results = res_json['data']

    return render_template('states_parks.html', results=results)

@app.route('/state/<state>/<park_id>', methods=["GET", "POST"])
def park_info(state, park_id):
    """Show info on specific park"""
    response = requests.get(f'{API_BASE_URL}parks?api_key={API_SECRET_KEY}&stateCode={state}&parkCode={park_id}')

    res_json = response.json()
    results = res_json['data']

    return render_template('park_info.html', results=results)

################# FAVORITES LIST ROUTES ###############

@app.route('/favorites/<park_id>', methods=["POST"])
def add_park_to_faves(park_id):
    """Add park to favorites"""
    user_id = g.user.id
    user = User.query.get_or_404(user_id)
    park = Park.query.get_or_404(park_id)

    add_park = FavoritePark(user_id=user.id, park_id=park.code)
    db.session.add(add_park)
    db.session.commit()

    flash("Park added to favorites!", "success")
    return redirect(url_for('park_info'))




###############
    # if not g.user:
    #     flash("Please login to add favorites.", "danger")
    #     return redirect("/")    

    # park = Park.query.get_or_404(park_id)
    # if not park:
    #     response = requests.get(f'{API_BASE_URL}parks?api_key={API_SECRET_KEY}&stateCode={state}&parkCode={park_id}')

    #     data = response.json()
    #     park = add_park_from_api(data)

    #     g.user.favorites.append(park)
    #     db.session.commit()
    # else:
    #     g.user.favorites.append(park)
    #     db.session.commit()
    # return jsonify(park=park.serialize())

###############
    # user_id = g.user.id
    # user = User.query.get_or_404(user_id)
    # park = Park.query.get_or_404(park_id)

    # in_faves = FavoritePark.query.filter_by(user_id=user.id, park_id=park.code)

    # if not in_faves:
    #     add_park = FavoritePark(user_id=user.id, park_id=park.code)
    #     db.session.add(add_park)
    #     db.session.commit()
    #     flash(f"{park.name} added to favorites!", "success")
    #     return redirect(url_for('park_info'))
    # else:
    #     flash("Park already in favorites.", "danger")
    #     return redirect(url_for('park_info'))



 










    



######## TESTING ########

API_BASE_URL = 'https://developer.nps.gov/api/v1/'

@app.route('/testing')
def test():

    response = requests.get(f"{API_BASE_URL}parks?limit=500&api_key={API_SECRET_KEY}")

    res_json = response.json()
    results = res_json['data']

    return render_template('testing.html', results=results)
  