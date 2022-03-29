from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to db"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Users table"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=True, unique=True)
    password = db.Column(db.String, nullable=False)

    favorites = db.relationship('FavoritePark')

    @classmethod
    def register(cls, username, password, email):
        """register user with hashed pw & return user"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode('utf8')

        #create user with hashed password
        user = User(username=username, password=hashed_utf8, email=email)
        db.session.add(user)

        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate user exists & login credentioals are right.
        Return user if valid, else return false """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u 
        else:
            return False 

class Park(db.Model):
    """Parks data from NPS API"""
    __tablename__ = 'parks'

    id = db.Column(db.Integer, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    code = db.Column(db.Text, primary_key=True, nullable=False)
    states = db.Column(db.Text, nullable=False)

    users = db.relationship('User', secondary='favorite_parks', backref='parks', lazy=True)
    favorites = db.relationship('FavoritePark')

    @property
    def park_name(self):
        return f'{self.name}'

    def serialize(self):
        """Returns a dict representation of parks to turn to JSON"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'states': self.states,
        }

    # states = db.relationship('State', secondary='parks_states', backref='parks')


class FavoritePark(db.Model):
    """Many to many users to parks"""
    __tablename__ = 'favorite_parks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), primary_key=True)
    park_id = db.Column(db.Text, db.ForeignKey('parks.code', ondelete='cascade'), primary_key=True)

    def __repr__(self):
        return f'<Favorite= user_id:{self.user_id} park_id:{self.park_id}>'



