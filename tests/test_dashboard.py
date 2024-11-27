def test_dashboard_access(client):
    """Test accessing the dashboard after login."""
    client.post('/admin/login', data={'username': 'admin', 'password': 'password'})
    response = client.get('/admin/dashboard')
    assert response.status_code == 200
    assert b'Admin Dashboard' in response.data

def test_dashboard_access_unauthenticated(client):
    """Test accessing the dashboard without login."""
    response = client.get('/admin/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b'Admin Login' in response.data
