from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from ..extensions import mongo
from app.utils.auth import login_required
from app.forms import LoginForm
from app.forms import SignupForm

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Create instance of the form
    if form.validate_on_submit():  # Use form's built-in validation
        username = form.username.data
        password = form.password.data

        # Find the admin user in the database
        admin = mongo.db.admins.find_one({'username': username})

        # Verify the password
        if admin and check_password_hash(admin['password_hash'], password):
            session['admin_id'] = str(admin['_id'])
            return redirect(url_for('admin.dashboard'))
        flash('Invalid credentials')
        
    return render_template('admin/login.html', form=form)

@admin_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()  # Create an instance of SignupForm
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        
        # Basic validation
        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('admin.signup'))
        
        # Check if the username already exists
        existing_admin = mongo.db.admins.find_one({'username': username})
        if existing_admin:
            flash('Username already exists.')
            return redirect(url_for('admin.signup'))

        # Save the new admin credentials securely
        mongo.db.admins.insert_one({
            'username': username,
            'password_hash': generate_password_hash(password)
        })
        flash('Signup successful! Please log in.')
        return redirect(url_for('admin.login'))
    
    return render_template('admin/signup.html', form=form)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/volunteers')
@login_required
def volunteer_management():
    volunteers = mongo.db.volunteers.find()
    return render_template('admin/volunteer_management.html', volunteers=volunteers)

@admin_bp.route('/events')
@login_required
def event_management():
    events = mongo.db.events.find()
    return render_template('admin/event_management.html', events=events)

@admin_bp.route('/awards')
@login_required
def award_management():
    volunteers = mongo.db.volunteers.find({'volunteer_hours': {'$gte': 20}})
    return render_template('admin/award_management.html', volunteers=volunteers)
