from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'Operational'}

def test_redoc():
    response = client.get('/redoc')
    assert response.status_code == status.HTTP_200_OK
    assert 'ReDoc' in response.text
