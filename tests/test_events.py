def test_event_list(client):
    """Test accessing the event management page."""
    client.post('/admin/login', data={'username': 'admin', 'password': 'password'})
    response = client.get('/admin/events')
    assert response.status_code == 200
    assert b'Event Management' in response.data

def test_edit_event(client):
    """Test editing an event."""
    client.post('/admin/login', data={'username': 'admin', 'password': 'password'})
    event_id = "event_test_id"  # replace with an actual event_id
    response = client.post(f'/admin/edit_event/{event_id}', data={
        'name': 'Updated Event',
        'date': '2024-12-01',
        'description': 'Updated Description'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Event updated successfully!' in response.data
