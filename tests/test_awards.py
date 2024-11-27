def test_award_management(client):
    """Test accessing the award management page."""
    client.post('/admin/login', data={'username': 'admin', 'password': 'password'})
    response = client.get('/admin/awards')
    assert response.status_code == 200
    assert b'Award Management' in response.data
