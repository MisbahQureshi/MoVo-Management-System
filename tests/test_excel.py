import io

def test_excel_export(client):
    """Test exporting data as an Excel file."""
    client.post('/admin/login', data={'username': 'admin', 'password': 'password'})
    response = client.get('/admin/export_excel?collections=volunteers', follow_redirects=True)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

def test_excel_import(client):
    """Test importing data from an Excel file."""
    client.post('/admin/login', data={'username': 'admin', 'password': 'password'})
    data = {
        'collection_name': 'volunteers',
        'file': (io.BytesIO(b"fake data"), 'fakefile.xlsx')
    }
    response = client.post('/admin/import_excel', content_type='multipart/form-data', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Data import failed.' in response.data  # Expecting failure with fake data
