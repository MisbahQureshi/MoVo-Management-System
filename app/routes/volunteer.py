from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import mongo  # Ensure the correct import path

volunteer_bp = Blueprint('volunteer', __name__)

@volunteer_bp.route('/register', methods=['GET', 'POST'])
def volunteer_registration():
    if request.method == 'POST':
        volunteer_data = {
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'email': request.form.get('email'),
            'student_id': request.form.get('student_id'),
            'contact_number': request.form.get('contact_number'),
            'volunteer_hours': 0
        }
        mongo.db.volunteers.insert_one(volunteer_data)
        flash('Registration successful!')
        return redirect(url_for('volunteer.volunteer_registration'))
    return render_template('volunteer/registration.html')

@volunteer_bp.route('/view')
def view_volunteers():
    volunteers = mongo.db.volunteers.find()
    return render_template('volunteer/view.html', volunteers=volunteers)
