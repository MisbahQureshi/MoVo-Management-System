from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils.auth import login_required  # Import login_required
from app.extensions import mongo

task_bp = Blueprint('task', __name__)

# Route: Task Management Page
@task_bp.route('/tasks', methods=['GET', 'POST'])
@login_required
def task_management():
    # Handling task creation
    if request.method == 'POST':
        task_name = request.form.get('task_name')
        task_description = request.form.get('task_description')
        task_date = request.form.get('task_date')
        task_event_id = request.form.get('task_event_id')
        volunteer_ids = request.form.getlist('task_volunteer_ids')

        if not task_name or not task_date or not task_event_id:
            flash("Task name, date, and associated event are required!", "error")
            return redirect(url_for('task.task_management'))

        try:
            # Generate a new task ID
            task_id = f"Task{mongo.db.tasks.count_documents({}) + 1:03d}"

            # Insert the new task into the database
            mongo.db.tasks.insert_one({
                'task_id': task_id,
                'name': task_name,
                'description': task_description,
                'date': task_date,
                'event_id': task_event_id,
                'volunteer_ids': volunteer_ids
            })
            flash('Task created successfully!', "success")
        except Exception as e:
            flash(f"An error occurred while creating the task: {e}", "error")

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
            'volunteer_ids': task.get('volunteer_ids', []),
            'event_id': task.get('event_id')
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

# Route: Edit Task
@task_bp.route('/edit_task/<task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = mongo.db.tasks.find_one({'task_id': task_id})

    if not task:
        flash("Task not found!", "error")
        return redirect(url_for('task.task_management'))

    if request.method == 'POST':
        updated_name = request.form.get('task_name')
        updated_description = request.form.get('task_description')
        updated_date = request.form.get('task_date')
        updated_event_id = request.form.get('task_event_id')
        updated_volunteer_ids = request.form.getlist('task_volunteer_ids')

        if not updated_name or not updated_date or not updated_event_id:
            flash("Task name, date, and associated event are required!", "error")
            return redirect(url_for('task.edit_task', task_id=task_id))

        try:
            # Update the task in the database
            mongo.db.tasks.update_one(
                {'task_id': task_id},
                {
                    '$set': {
                        'name': updated_name,
                        'description': updated_description,
                        'date': updated_date,
                        'event_id': updated_event_id,
                        'volunteer_ids': updated_volunteer_ids
                    }
                }
            )
            flash("Task updated successfully!", "success")
        except Exception as e:
            flash(f"An error occurred while updating the task: {e}", "error")

        return redirect(url_for('task.task_management'))

    events = list(mongo.db.events.find())
    volunteers = list(mongo.db.volunteers.find())

    return render_template(
        'admin/edit_task.html',
        task=task,
        events=events,
        volunteers=volunteers
    )

# Route: Delete Task
@task_bp.route('/delete_task/<task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    try:
        # Delete the task from the database
        mongo.db.tasks.delete_one({'task_id': task_id})
        flash("Task deleted successfully!", "success")
    except Exception as e:
        flash(f"An error occurred while deleting the task: {e}", "error")

    return redirect(url_for('task.task_management'))
