from crypt import methods
from sqlite3 import IntegrityError
from flask import Flask, render_template, g, redirect, session, request, flash, jsonify, make_response, url_for
from flask_wtf import FlaskForm
from helpers import random_quote
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Park, FavoritePark
from forms import CreateUserForm, LoginForm, EditUser
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

############ BASIC ROUTES #############

@app.route('/')
def root():
    """Basic homepage reroute"""
    return redirect('/home')

@app.route('/home')
def homepage():
    """Actual omepage"""
    popular = ['grsm', 'zion', 'yell', 'grca', 'romo', 'acad']
    results = []

    for pop in popular:
        response = requests.get(f'{API_BASE_URL}parks?api_key={API_SECRET_KEY}&parkCode={pop}')
        res_json = response.json()
        results.append(res_json['data'][0])

    return render_template('home.html', results=results)


############# USER ROUTES #############

@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Register a new user"""
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
            return redirect('/home')

        flash("Username/Password incorrect.", "danger")
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logging a user out"""
    do_logout()
    flash("See you next time!", 'success')
    return redirect('/')


@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user(user_id):
    """Edit user profile info"""
    if not g.user:
        flash("Unauthorized acces.", 'danger')
        return redirect('/')

    user = User.query.get(user_id)
    form = EditUser(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash(f"Account successfully updated!", 'success')
        return redirect(f"/users/{user.id}")

    return render_template('users_edit.html', form=form, user=user)


@app.route('/users/<int:user_id>')
def users_page(user_id):
    """Show user profile"""
    user = User.query.get_or_404(user_id)
    return render_template('users.html', user=user)


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user"""
    if not g.user:
        flash("Unauthorized acces.", 'danger')
        return redirect('/')
    
    user = User.query.get_or_404(user_id)
    faves = FavoritePark.query.filter_by(user_id=user.id).all()
    for fave in faves:
        db.session.delete(fave)
    db.session.delete(user)
  
    db.session.commit()
    session.pop(CURR_USER_KEY)
    flash(f"{g.user.username} has been deleted.", 'secondary')
    return redirect('/')


############### PARK ROUTES ###############

@app.route('/state/<state>')
def lookup_state(state):
    """Show parks based on specific state(s)"""
    response = requests.get(f'{API_BASE_URL}parks?api_key={API_SECRET_KEY}&stateCode={state}')

    res_json = response.json()
    results = res_json['data']

    rand = random_quote()

    return render_template('states_parks.html', results=results, rand=rand)

@app.route('/state/<state>/<park_id>')
def park_info(state, park_id):
    """Show specific park information"""
    response = requests.get(f'{API_BASE_URL}parks?api_key={API_SECRET_KEY}&stateCode={state}&parkCode={park_id}')

    res_json = response.json()
    results = res_json['data']

    alert_res = requests.get(f'{API_BASE_URL}alerts?api_key={API_SECRET_KEY}&parkCode={park_id}')
    alert_res_json = alert_res.json()
    alerts = alert_res_json['data']

    return render_template('park_info.html', results=results, alerts=alerts)

################# FAVORITES LIST ROUTES ###############

@app.route('/state/<state>/<park_id>', methods=["POST"])
def add_park_to_faves(state, park_id):
    """Add park to user favorites"""

    if not g.user:
        flash("Please log in to add to favorites!", 'danger')
        return redirect('/state/<state>/<park_id>')

    response = requests.get(f'{API_BASE_URL}parks?api_key={API_SECRET_KEY}&stateCode={state}&parkCode={park_id}')

    res_json = response.json()
    results = res_json['data']

    user_id = g.user.id
    user = User.query.get_or_404(user_id)
    park = Park.query.get_or_404(park_id)

    fave = FavoritePark.query.filter_by(user_id=user.id, park_id=park.code).first()

    if not fave:
        res = requests.get(f'{API_BASE_URL}parks?api_key={API_SECRET_KEY}&parkCode={park_id}')
        res_json = res.json()
        results = res_json['data']

        add_park = FavoritePark(user_id=user.id, park_id=park.code)
        
        db.session.add(add_park)
        db.session.commit()
        flash("Park added to favorites!", 'success')
        return render_template('park_info.html', results=results)

    else:
        flash("Park already in favorites!", 'danger')
        return render_template('park_info.html', results=results)

@app.route('/favorites/delete/<park_id>', methods=["GET", "POST"])
def delete_fave(park_id):
    """Delete a park from user favorites"""
    fave = FavoritePark.query.filter_by(user_id=g.user.id, park_id=park_id).first()
    db.session.delete(fave)
    db.session.commit()
    flash("Park removed from favorites.", 'success')

    return redirect('/favorites')


@app.route("/favorites")
def show_favorites():
    """View all parks in users favorites"""
    if not g.user:
        flash("You need to login to view favorites.", "danger")
        return redirect('/login')

    user_id = g.user.id
    user = User.query.get_or_404(user_id)
    user_faves = user.favorites

    faves = [p.park_id for p in user_faves]
    results = []

    for park in faves:
        res = requests.get(f'{API_BASE_URL}parks?api_key={API_SECRET_KEY}&parkCode={park}')
        res_json = res.json()
        results.append(res_json['data'][0])

    return render_template('favorite_parks.html', faves=faves, user=user, results=results)

  