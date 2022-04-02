from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class CreateUserForm(FlaskForm):
    """Form for creating a new user"""
    email = StringField('Email')
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class LoginForm(FlaskForm):
    """Login form for users"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class EditUser(FlaskForm):
    """Edit user details form"""
    username = StringField('Username')
    email = StringField('Email')