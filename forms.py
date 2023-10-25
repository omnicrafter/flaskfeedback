from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length


class UserForm(FlaskForm):
    username = StringField("Username", validators=[
                           InputRequired(message="Please enter a username")])
    password = PasswordField("Password", validators=[
                             InputRequired(message="Please enter a password")])


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
                           InputRequired(message="Please enter a username"), Length(max=20)])
    password = PasswordField("Password", validators=[
                             InputRequired(message="Please enter a password")])
    email = EmailField("Email", validators=[InputRequired(
        message="Please enter a valid email"), Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(
        message="Please enter your first name"), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(
        message="Please enter your last name"), Length(max=30)])


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
                           InputRequired(message="Please enter a username"), Length(max=20)])
    password = PasswordField("Password", validators=[
                             InputRequired(message="Please enter a password")])
