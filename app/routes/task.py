from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils.auth import login_required  # Import login_required
from app.extensions import mongo
from bson import ObjectId

task_bp = Blueprint('task', __name__)

# Route: Task Management Page
@task_bp.route('/tasks', methods=['GET', 'POST'])
@login_required  # This decorator ensures only logged-in users can access this route
def task_management():
    # Handling task creation
    if request.method == 'POST':
        task_name = request.form.get('task_name')
        task_description = request.form.get('task_description')
        task_date = request.form.get('task_date')
        task_event_id = request.form.get('task_event_id')  # Event ID selected from dropdown
        volunteer_ids = request.form.getlist('task_volunteer_ids')  # List of volunteer IDs selected

        if not task_name or not task_date or not task_event_id:
            flash("Task name, date, and associated event are required!", "error")
            return redirect(url_for('task.task_management'))

        try:
            # Generate a new task ID based on the count of existing tasks
            task_id = f"Task{mongo.db.tasks.count_documents({}) + 1:03d}"

            # Insert the new task into the database
            mongo.db.tasks.insert_one({
                'task_id': task_id,
                'name': task_name,
                'description': task_description,
                'date': task_date,
                'event_id': task_event_id,
                'volunteer_ids': volunteer_ids  # Assign selected volunteers
            })
            flash('Task created successfully!', "success")
        except Exception as e:
            flash(f"An error occurred while creating the task: {e}", "error")

        return redirect(url_for('task.task_management'))

    # Handling task deletion
    if request.args.get('action') == 'delete':
        task_id = request.args.get('task_id')
        try:
            mongo.db.tasks.delete_one({'task_id': task_id})  # Delete task by task_id
            flash("Task deleted successfully!", "success")
        except Exception as e:
            flash(f"An error occurred while deleting the task: {e}", "error")

        return redirect(url_for('task.task_management'))

    # Fetch all tasks for display
    tasks = list(mongo.db.tasks.find())
    tasks_list = []
    for task in tasks:
        tasks_list.append({
            'task_id': task.get('task_id'),
            'name': task.get('name'),
            'description': task.get('description'),
            'date': task.get('date'),
            'volunteer_ids': task.get('volunteer_ids', []),  # List of volunteer IDs assigned
            'event_id': task.get('event_id')  # Associated event ID
        })

    # Fetch all events for the event dropdown
    events = list(mongo.db.events.find())

    # Fetch all volunteers for the volunteers dropdown
    volunteers = list(mongo.db.volunteers.find())

    return render_template(
        'admin/task_management.html',
        tasks=tasks_list,
        events=events,
        volunteers=volunteers
    )
