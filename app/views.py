from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash  # Import this for hashing passwords
from app.models import Admin, Volunteer, Event
from app.forms import LoginForm, SignupForm, UploadForm, EventForm
import os
import pandas as pd

# Blueprint setup
main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def home():
    if 'admin' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if Admin.verify_admin(username, password):
            session['admin'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html', form=form)

@main_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check if the username already exists
        existing_admin = Admin.get_admin_by_username(username)
        if existing_admin:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            # Create a new admin with the hashed password
            hashed_password = generate_password_hash(password)
            Admin.create_admin(username, hashed_password)
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('main.login'))
    return render_template('signup.html', form=form)

@main_blueprint.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect(url_for('main.login'))
    volunteers = Volunteer.get_all_volunteers()
    events = Event.get_all_events()
    return render_template('dashboard.html', volunteers=volunteers, events=events)

@main_blueprint.route('/logout')
def logout():
    session.pop('admin', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@main_blueprint.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'admin' not in session:
        return redirect(url_for('main.login'))

    form = UploadForm()
    if form.validate_on_submit():
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            file.save(os.path.join('/tmp', filename))
            
            # Read the CSV file and process the data
            data = pd.read_csv(os.path.join('/tmp', filename))
            for _, row in data.iterrows():
                volunteer_data = {
                    'roll_number': row['Roll Number'],
                    'name': row['Name'],
                    'hours': row['Hours Volunteered']
                }
                existing_volunteer = Volunteer.get_volunteer_by_roll_number(row['Roll Number'])
                if existing_volunteer:
                    Volunteer.update_volunteer_hours(row['Roll Number'], row['Hours Volunteered'])
                else:
                    Volunteer.add_volunteer(volunteer_data)
            
            flash('File successfully uploaded and data saved to the database.', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid file type. Please upload a CSV file.', 'danger')
    
    return render_template('upload.html', form=form)

@main_blueprint.route('/add_event', methods=['POST'])
def add_event():
    if 'admin' not in session:
        return redirect(url_for('main.login'))
    
    form = EventForm()
    if form.validate_on_submit():
        event_data = {
            'event_id': form.event_id.data,
            'event_name': form.event_name.data,
            'date': form.date.data,
            'description': form.description.data
        }
        Event.add_event(event_data)
        flash('Event successfully added!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('add_event.html', form=form)
