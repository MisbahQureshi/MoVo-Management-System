from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import mongo

volunteer_bp = Blueprint('volunteer', __name__)

# Volunteer registration route
@volunteer_bp.route('/register', methods=['GET', 'POST'])
def volunteer_registration():
    if request.method == 'POST':
        # Collecting form data for volunteer registration
        volunteer_data = {
            'volunteer_id': request.form.get('volunteer_id'),  # Assuming a unique volunteer ID
            'name': f"{request.form.get('first_name')} {request.form.get('last_name')}",
            'email': request.form.get('email'),
            'student_id': request.form.get('student_id'),
            'contact_number': request.form.get('contact_number'),
            'volunteer_hours': 0,  # Initially set to 0
            'status': 'active',  # Default status is active
            'event_id': [],  # List of event IDs the volunteer is associated with
            'schedule': [],  # List of event schedules for the volunteer
            'awards_id': [],  # Initially empty list for awards
        }

        try:
            mongo.db.volunteers.insert_one(volunteer_data)
            flash('Registration successful!')
            return redirect(url_for('volunteer.volunteer_registration'))
        except Exception as e:
            flash(f'An error occurred while registering: {str(e)}')

    return render_template('volunteer/registration.html')

# View all volunteers route
@volunteer_bp.route('/view')
def view_volunteers():
    # Fetching all volunteer data from the database
    volunteers = mongo.db.volunteers.find()

    # Prepare volunteers data with necessary fields
    volunteers_list = []
    for volunteer in volunteers:
        volunteers_list.append({
            'volunteer_id': volunteer.get('volunteer_id'),
            'name': volunteer.get('name'),
            'email': volunteer.get('email'),
            'volunteer_hours': volunteer.get('volunteer_hours'),
            'status': volunteer.get('status'),
            'student_id': volunteer.get('student_id'),
            'contact_number': volunteer.get('contact_number'),
            'event_ids': volunteer.get('event_id', []),  # Associated event IDs
            'schedule': volunteer.get('schedule', []),  # Schedule for events
            'awards_id': volunteer.get('awards_id', []),  # Awards associated with the volunteer
        })
    
    return render_template('volunteer/view.html', volunteers=volunteers_list)