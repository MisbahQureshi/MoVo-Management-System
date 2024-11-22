from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from bson import ObjectId
from app.extensions import mongo
from app.models.event import Event
from app.models.volunteer import Volunteer

event_bp = Blueprint('event', __name__)

def generate_event_id():
    """Generate a new event ID based on the existing events in the database."""
    try:
        # Fetch all event IDs and sort them in descending order
        last_event = mongo.db.events.find_one(sort=[("event_id", -1)])
        if last_event and "event_id" in last_event:
            # Extract the numeric part of the last event ID and increment it
            last_id_num = int(last_event["event_id"][3:])
            new_id_num = last_id_num + 1
        else:
            # Start from 1 if no events exist
            new_id_num = 1
        # Return the new event ID in the format "EvnXXX"
        return f"Evn{new_id_num:03d}"
    except Exception as e:
        flash(f"Error generating event ID: {str(e)}")
        return None

# Route: Create Event
@event_bp.route('/create', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('event_name')
        description = request.form.get('description')
        date = request.form.get('date')  # Event date field
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        assigned_volunteers = request.form.getlist('volunteers')  # List of selected volunteer IDs

        # Validation
        if not name or not date or not start_date or not end_date:
            flash('Event name, event date, start date, and end date are required.')
            return redirect(url_for('event.create_event'))

        # Check if the user is logged in (either as admin or employee)
        if 'admin_id' in session:
            employee_id = 'admin'  # Admin user
        elif 'employee_id' in session:
            employee_id = session['employee_id']  # Employee ID from session
        else:
            flash('Please log in first!')
            return redirect(url_for('admin.login'))

        # Generate a new event ID
        event_id = generate_event_id()
        if not event_id:
            flash("Failed to generate event ID. Please try again.")
            return redirect(url_for('event.create_event'))

        # Create event data - Ensure it matches the correct format in the DB
        event_data = {
            'event_id': event_id,
            'name': name,
            'description': description,
            'date': date,  # Store the event date separately
            'start_date': start_date,
            'end_date': end_date,
            'volunteer_id': assigned_volunteers,  # Use 'volunteer_id' as per the correct structure
            'employee_id': employee_id
        }

        try:
            mongo.db.events.insert_one(event_data)
            flash('Event created successfully!')
            return redirect(url_for('admin.event_management'))  # Correct redirect to admin's event management
        except Exception as e:
            flash(f'Failed to create event. Error: {str(e)}')
            return redirect(url_for('event.create_event'))

    # Retrieve all volunteers to display in the form
    volunteers = list(Volunteer.find_all())
    return render_template('admin/create_event.html', volunteers=volunteers)

# Route: Assign Tasks to Volunteers
@event_bp.route('/assign-tasks', methods=['GET', 'POST'])
def assign_tasks():
    if request.method == 'POST':
        event_id = request.form.get('event_id')
        task_name = request.form.get('task_name')
        assigned_to = request.form.get('assigned_to')

        # Validation
        if not event_id or not task_name or not assigned_to:
            flash('Event, task name, and volunteer assignment are required.')
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

# Route: Display Events (with all details)
@event_bp.route('/events', methods=['GET'])
def events():
    try:
        # Fetch all events
        events = mongo.db.events.find()
        # Convert to a list of dictionaries
        events_list = []
        for event in events:
            events_list.append({
                'id': str(event['_id']),
                'event_id': event.get('event_id'),
                'name': event.get('name'),  # Use 'name' from the database
                'description': event.get('description'),
                'start_date': event.get('start_date'),
                'end_date': event.get('end_date'),
                'volunteers': event.get('volunteer_id', []),  # Display volunteer IDs
                'tasks': event.get('tasks', [])
            })

        return render_template('admin/event_management.html', events=events_list)

    except Exception as e:
        flash(f'Error fetching events: {str(e)}')
        return redirect(url_for('admin.event_management'))
