from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField, BooleanField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from movieRecFlask.auth.models import User
# pip3 install Flask-WTF


def email_exists(form, field):
    email = User.query.filter_by(user_email=field.data).first()
    if email:
        raise ValidationError('Email already exists!')


class RegistrationForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired(),
                                           Length(3, 15, message='Name must be between 3 and 15 characters long')])
    email = StringField('E-mail', validators=[DataRequired(), Email(), email_exists])
    password = PasswordField('Password', validators=[DataRequired(), Length(4),
                                                     EqualTo('confirm', message='password must match')])
    confirm = PasswordField('Confirm', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    stay_loggedin = BooleanField('stay logged in')
    submit = SubmitField('Log In')