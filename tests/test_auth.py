import pytest
from app import create_app
from app.extensions import mongo

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = "mongodb://localhost:27017/test_db"  # Use a separate test DB
    with app.test_client() as client:
        yield client

def test_login_page(client):
    """Test that the login page loads correctly."""
    response = client.get('/admin/login')
    assert response.status_code == 200
    assert b'Admin Login' in response.data

def test_successful_login(client):
    """Test login with valid credentials."""
    response = client.post('/admin/login', data={
        'username': 'admin',
        'password': 'password'  # replace with a valid username/password in your test DB
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Admin Dashboard' in response.data

def test_logout(client):
    """Test logout functionality."""
    client.post('/admin/login', data={'username': 'admin', 'password': 'password'})
    response = client.get('/admin/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Admin Login' in response.data
