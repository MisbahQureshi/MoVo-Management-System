from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import mongo
from bson import ObjectId

volunteer_bp = Blueprint('volunteer', __name__)

# Volunteer registration route
@volunteer_bp.route('/register', methods=['POST'])
def volunteer_registration():
    if request.method == 'POST':
        # Collect form data
        time_in = request.form.get('time_in')
        time_out = request.form.get('time_out')

        # Calculate volunteer hours
        if time_in and time_out:
            try:
                from datetime import datetime

                time_in_dt = datetime.strptime(time_in, "%H:%M")
                time_out_dt = datetime.strptime(time_out, "%H:%M")
                time_diff = (time_out_dt - time_in_dt).total_seconds() / 3600  # Convert seconds to hours

                if time_diff <= 0:
                    flash("Time Out must be later than Time In", 'error')
                    return redirect(url_for('volunteer.volunteer_registration'))

                volunteer_hours = round(time_diff, 2)
            except Exception as e:
                flash(f"Error calculating volunteer hours: {e}", 'error')
                return redirect(url_for('volunteer.volunteer_registration'))
        else:
            flash("Both Time In and Time Out are required", 'error')
            return redirect(url_for('volunteer.volunteer_registration'))

        volunteer_data = {
            'volunteer_id': f"Vol{mongo.db.volunteers.count_documents({}) + 1:03d}",  # Auto-generate ID
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'volunteer_hours': int(request.form.get('volunteer_hours', 0)),
            'status': request.form.get('status', 'active'),
            'student_id': request.form.get('student_id'),
            'award_id': request.form.get('award_id', '').split(','),
            'event_id': request.form.get('event_id', '').split(','),
            'schedule': []
        }

        # Parse and validate schedule field
        schedule_data = request.form.get('schedule')
        if schedule_data:
            for entry in schedule_data.splitlines():
                try:
                    event_id, start_date, end_date = entry.split(',')
                    volunteer_data['schedule'].append({
                        'event_id': event_id.strip(),
                        'start_date': start_date.strip(),
                        'end_date': end_date.strip()
                    })
                except ValueError:
                    flash(f"Invalid schedule format for entry: {entry}", 'error')

        # Insert volunteer into database
        try:
            mongo.db.volunteers.insert_one(volunteer_data)
            flash('Volunteer added successfully!', 'success')
        except Exception as e:
            flash(f"Error while adding volunteer: {e}", 'error')

    return redirect(url_for('admin.volunteer_management'))


# View all volunteers route
@volunteer_bp.route('/view')
def view_volunteers():
    # Fetch all volunteers from the database
    volunteers = mongo.db.volunteers.find()

    # Prepare volunteers for rendering
    volunteers_list = [
        {
            'volunteer_id': volunteer.get('volunteer_id'),
            'name': volunteer.get('name'),
            'email': volunteer.get('email'),
            'volunteer_hours': volunteer.get('volunteer_hours'),
            'status': volunteer.get('status'),
            'student_id': volunteer.get('student_id'),
            'phone': volunteer.get('phone'),
            'event_id': volunteer.get('event_id', []),
            'awards_id': volunteer.get('awards_id', []),
            'schedule': volunteer.get('schedule', [])
        }
        for volunteer in volunteers
    ]

    return render_template('volunteer/view.html', volunteers=volunteers_list)
