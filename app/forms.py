from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectMultipleField  # Add SelectMultipleField here
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UploadForm(FlaskForm):
    file = FileField('Upload CSV File', validators=[DataRequired()])
    submit = SubmitField('Upload')

class EventForm(FlaskForm):
    event_name = StringField('Event Name', validators=[DataRequired(), Length(max=100)])
    date = StringField('Date', validators=[DataRequired(), Length(max=10)])
    description = StringField('Description', validators=[Length(max=500)])
    volunteer_id = SelectMultipleField('Select Volunteers', coerce=str)  # For multiple volunteer selection
    submit = SubmitField('Add Event')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
