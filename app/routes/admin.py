# app/routes/admin.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app.utils.bcrypt_utils import generate_password_hash, check_password_hash
from app.forms import LoginForm, SignupForm
from app.utils.auth import login_required, set_session_timeout
from app.extensions import mongo
from bson import ObjectId
from datetime import datetime
from app.utils.excel_utils import ExcelHandler  # Importing the ExcelHandler to handle export and import

admin_bp = Blueprint('admin', __name__)

# Admin login route
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        admin = mongo.db.admins.find_one({'username': username})

        if admin and check_password_hash(admin['password_hash'], password):
            session['admin_id'] = str(admin['_id'])
            set_session_timeout()  # Set session timeout after successful login
            return redirect(url_for('admin.dashboard'))

              # Check if user is an employee
        employee = mongo.db.employee.find_one({'username': username})

        if employee and check_password_hash(employee['password_hash'], password):
            session['employee_id'] = str(employee['_id'])
            set_session_timeout()
            return redirect(url_for('admin.dashboard'))
        flash('Invalid credentials')

    return render_template('admin/login.html', form=form)

# Admin logout route
@admin_bp.route('/logout')
@login_required
def logout():
    session.clear()  # Clear the session to log out
    response = redirect(url_for('admin.login'))
    response.set_cookie('session', value='', expires=0)
    response.delete_cookie('session')  # Delete the session cookie from the client side
    flash('You have been logged out.')
    return response

# Admin signup route
@admin_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        
        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('admin.signup'))

        existing_admin = mongo.db.admins.find_one({'username': username})
        if existing_admin:
            flash('Username already exists.')
            return redirect(url_for('admin.signup'))

        mongo.db.admins.insert_one({
            'username': username,
            'password_hash': generate_password_hash(password)
        })
        flash('Signup successful! Please log in.')
        return redirect(url_for('admin.login'))
    
    return render_template('admin/signup.html', form=form)

# Admin dashboard route
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')

# Volunteer management route
@admin_bp.route('/volunteers')
@login_required
def volunteer_management():
    volunteers = mongo.db.volunteers.find()
    return render_template('admin/volunteer_management.html', volunteers=volunteers)

# Event management route
@admin_bp.route('/events')
@login_required
def event_management():
    events = mongo.db.events.find()
    return render_template('admin/event_management.html', events=events)

# Award management route
@admin_bp.route('/awards')
@login_required
def award_management():
    volunteers = mongo.db.volunteers.find({'volunteer_hours': {'$gte': 20}})
    return render_template('admin/award_management.html', volunteers=volunteers)

# Edit volunteer route
@admin_bp.route('/edit_volunteer/<volunteer_id>', methods=['GET', 'POST'])
@login_required
def edit_volunteer(volunteer_id):
    volunteer = mongo.db.volunteers.find_one({'_id': ObjectId(volunteer_id)})
    
    if request.method == 'POST':
        updated_name = request.form.get('name')
        updated_email = request.form.get('email')
        updated_hours = request.form.get('volunteer_hours')
        
        mongo.db.volunteers.update_one(
            {'_id': ObjectId(volunteer_id)},
            {'$set': {
                'name': updated_name,
                'email': updated_email,
                'volunteer_hours': int(updated_hours)
            }}
        )
        
        flash('Volunteer updated successfully!')
        return redirect(url_for('admin.volunteer_management'))
    
    return render_template('admin/edit_volunteer.html', volunteer=volunteer)

# Delete volunteer route
@admin_bp.route('/delete_volunteer/<volunteer_id>', methods=['POST'])
@login_required
def delete_volunteer(volunteer_id):
    try:
        mongo.db.volunteers.delete_one({'_id': ObjectId(volunteer_id)})
        flash('Volunteer deleted successfully!')
    except Exception as e:
        flash(f'An error occurred while deleting the volunteer: {str(e)}')
    
    return redirect(url_for('admin.volunteer_management'))

# Edit event route
@admin_bp.route('/edit_event/<event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = mongo.db.events.find_one({'_id': ObjectId(event_id)})
    
    # Format the date if it exists and is in ISO format
    if event and isinstance(event.get('date'), str):
        try:
            event['date'] = datetime.fromisoformat(event['date']).strftime('%Y-%m-%d')
        except ValueError:
            event['date'] = ''

    if request.method == 'POST':
        updated_name = request.form.get('name')
        updated_date = request.form.get('date')
        updated_description = request.form.get('description')
        
        mongo.db.events.update_one(
            {'_id': ObjectId(event_id)},
            {'$set': {
                'name': updated_name,
                'date': updated_date,
                'description': updated_description
            }}
        )
        
        flash('Event updated successfully!')
        return redirect(url_for('admin.event_management'))
    
    return render_template('admin/edit_event.html', event=event)

# Delete event route
@admin_bp.route('/delete_event/<event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    try:
        mongo.db.events.delete_one({'_id': ObjectId(event_id)})
        flash('Event deleted successfully!')
    except Exception as e:
        flash(f'An error occurred while deleting the event: {str(e)}')
    
    return redirect(url_for('admin.event_management'))

# Route to manage Excel data (export/import)
@admin_bp.route('/excel', methods=['GET', 'POST'])
@login_required
def excel_management():
    if request.method == 'POST':
        # Handle Excel import
        collection_name = request.form.get('collection_name')
        if collection_name:
            result = ExcelHandler.import_from_excel(collection_name)
            if result:
                flash(f"Data successfully imported into {collection_name} collection.")
            else:
                flash("An error occurred while importing data.")
    return render_template('admin/excel_management.html')

# Export Excel route
@admin_bp.route('/export_excel', methods=['GET'])
@login_required
def export_excel():
    collections = request.args.getlist('collections')
    sheet_names = request.args.getlist('sheet_names')  # Optional: Use custom sheet names
    
    if not collections:
        flash("No collections selected!")
        return redirect(url_for('admin.excel_management'))
    
    # Call ExcelHandler to export the data
    return ExcelHandler.export_to_excel(collections, sheet_names)

# Import Excel route
@admin_bp.route('/import_excel', methods=['POST'])
@login_required
def import_excel():
    collection_name = request.form.get('collection_name')
    
    if not collection_name:
        flash("No collection selected for import!")
        return redirect(url_for('admin.excel_management'))
    
    # Call ExcelHandler to import the data
    result = ExcelHandler.import_from_excel(collection_name)
    if result:
        flash("Data imported successfully!")
    else:
        flash("Data import failed.")
    
    return redirect(url_for('admin.excel_management'))
