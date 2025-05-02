from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField, BooleanField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired,  NumberRange, Length, ValidationError
from flask_wtf.file import FileAllowed, FileRequired

from datetime import datetime

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Fullname', validators=[DataRequired()]) 
    email = StringField('Email', validators=[DataRequired()])

    photo =  FileField('Profile Picture', validators=[FileRequired(),
        FileAllowed(['jpg', 'png'], message="Images only! (jpg, png, jpeg)")
    ])

    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Username is required")])
    password = PasswordField('Password', validators=[DataRequired(message="Password is required")])
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired(), Length(max=200, message="Description must be less than 200 characters")])
    parish = StringField('Parish', validators=[DataRequired()])
    biography = TextAreaField('Biography', validators=[DataRequired(), Length(max=1000, message="Biography must be less than 1000 characters")])
    sex = SelectField('Sex', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    race = SelectField('Race', choices=[('White', 'White'), ('Black', 'Black'), ('Hispanic', 'Hispanic'), ('Asian', 'Asian'), ('Other', 'Other')], validators=[DataRequired()])
    birth_year = IntegerField('Birth Year', validators=[DataRequired(), NumberRange(min=1900, max=2025, message="Please enter a valid year")])
    height = FloatField('Height (in cm)', validators=[DataRequired(), NumberRange(min=100, max=250, message="Height should be between 100cm and 250cm")])
    fav_cuisine = StringField('Favorite Cuisine', validators=[DataRequired()])
    fav_colour = StringField('Favorite Color', validators=[DataRequired()])
    fav_school_subject = StringField('Favorite School Subject', validators=[DataRequired()])
    political = BooleanField('Political', default=False)
    religious = BooleanField('Religious', default=False)
    family_oriented = BooleanField('Family Oriented', default=False)

    submit = SubmitField('Save Profile')