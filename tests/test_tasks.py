def test_task_management(client):
    """Test accessing the task management page."""
    client.post('/admin/login', data={'username': 'admin', 'password': 'password'})
    response = client.get('/task/tasks')
    assert response.status_code == 200
    assert b'Task Management' in response.data

def test_add_task(client):
    """Test adding a new task."""
    client.post('/admin/login', data={'username': 'admin', 'password': 'password'})
    response = client.post('/task/tasks', data={
        'task_name': 'New Task',
        'task_date': '2024-11-30'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Task created successfully!' in response.data
