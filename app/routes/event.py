from flask import Blueprint, render_template, request, redirect, url_for, flash
from bson import ObjectId
from app.extensions import mongo

event_bp = Blueprint('event', __name__)

@event_bp.route('/create', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        # Retrieve form data
        event_name = request.form.get('event_name')
        event_date = request.form.get('event_date')

        # Basic validation
        if not event_name or not event_date:
            flash('Event name and date are required.')
            return redirect(url_for('event.create_event'))

        # Prepare event data
        event_data = {
            'event_name': event_name,
            'event_date': event_date,
            'volunteers': [],
            'tasks': []
        }

        try:
            # Insert the new event into the database
            mongo.db.events.insert_one(event_data)
            flash('Event created successfully!')
        except Exception as e:
            flash(f'An error occurred: {str(e)}')
            return redirect(url_for('event.create_event'))

        return redirect(url_for('event.create_event'))

    return render_template('event/create.html')

@event_bp.route('/assign-tasks', methods=['GET', 'POST'])
def assign_tasks():
    if request.method == 'POST':
        event_id = request.form.get('event_id')
        task_name = request.form.get('task_name')
        assigned_to = request.form.get('assigned_to')

        # Basic validation
        if not event_id or not task_name or not assigned_to:
            flash('All fields are required.')
            return redirect(url_for('event.assign_tasks'))

        # Prepare task data
        task_data = {
            'task_name': task_name,
            'assigned_to': assigned_to,
            'status': 'pending'
        }

        try:
            # Convert event_id to ObjectId
            event_obj_id = ObjectId(event_id)
            # Add the task to the event's tasks array
            mongo.db.events.update_one(
                {'_id': event_obj_id},
                {'$push': {'tasks': task_data}}
            )
            flash('Task assigned successfully!')
        except Exception as e:
            flash(f'An error occurred: {str(e)}')
            return redirect(url_for('event.assign_tasks'))

        return redirect(url_for('event.assign_tasks'))

    # Retrieve events and volunteers for the dropdowns
    events = mongo.db.events.find()
    volunteers = mongo.db.volunteers.find()
    return render_template('event/assign_tasks.html', events=events, volunteers=volunteers)
