def test_volunteer_list(client):
    """Test accessing the volunteer management page."""
    client.post('/admin/login', data={'username': 'admin', 'password': 'password'})
    response = client.get('/admin/volunteers')
    assert response.status_code == 200
    assert b'Volunteer Management' in response.data

def test_add_volunteer(client):
    """Test adding a new volunteer."""
    client.post('/admin/login', data={'username': 'admin', 'password': 'password'})
    response = client.post('/admin/volunteers', data={
        'name': 'John Doe',
        'email': 'john@example.com',
        'volunteer_hours': 10
    })
    assert response.status_code == 302  # Should redirect after adding
