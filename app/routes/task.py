from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils.auth import login_required  # Import login_required
from app.extensions import mongo
from bson import ObjectId

task_bp = Blueprint('task', __name__)

# Route: Task Management Page
@task_bp.route('/tasks', methods=['GET', 'POST'])
@login_required  # This decorator ensures only logged-in users can access this route
def task_management():
    # Fetch all tasks
    tasks = mongo.db.tasks.find()
    tasks_list = []
    
    for task in tasks:
        tasks_list.append({
            'task_id': task.get('task_id'),
            'name': task.get('name'),
            'description': task.get('description'),
            'date': task.get('date'),
            'volunteer_ids': task.get('volunteer_ids', []),  # List of volunteer IDs assigned
            'event_id': task.get('event_id')
        })
    
    # Handling task creation
    if request.method == 'POST':
        task_name = request.form.get('task_name')
        task_description = request.form.get('task_description')
        task_date = request.form.get('task_date')
        task_event_id = request.form.get('task_event_id')
        volunteer_ids = request.form.getlist('task_volunteer_ids')  # List of volunteer IDs for this task
        
        if not task_name or not task_date:
            flash("Task name and date are required!")
            return redirect(url_for('task.task_management'))
        
        try:
            # Create new task in the database
            task_id = f"Task{str(mongo.db.tasks.count_documents({}) + 1)}"  # Generate task ID based on existing tasks count
            mongo.db.tasks.insert_one({
                'task_id': task_id,
                'name': task_name,
                'description': task_description,
                'date': task_date,
                'event_id': task_event_id,
                'volunteer_ids': volunteer_ids  # Assign volunteers to the task
            })
            flash('Task created successfully!')
        except Exception as e:
            flash(f"An error occurred: {str(e)}")
        
        return redirect(url_for('task.task_management'))

    # Handling task deletion
    if request.args.get('action') == 'delete':
        task_id = request.args.get('task_id')
        try:
            mongo.db.tasks.delete_one({'task_id': task_id})  # Delete by task_id
            flash("Task deleted successfully!")
        except Exception as e:
            flash(f"An error occurred: {str(e)}")
        
        return redirect(url_for('task.task_management'))

    return render_template('admin/task_management.html', tasks=tasks_list)
