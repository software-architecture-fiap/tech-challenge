from types import SimpleNamespace
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_auth_success(mocker):
    mock_user = SimpleNamespace(id=1, email='user@example.com', hashed_password='$2b$12$125as3fd45gdas5')

    mocker.patch('app.services.repository.get_user_by_email', return_value=mock_user)
    mocker.patch('app.services.security.verify_password', return_value=True)
    mocker.patch('app.services.security.create_access_token', return_value='bearer mock_access_token')

    form_data = {'username': 'user@example.com', 'password': 'valid_password'}

    response = client.post('/token', data=form_data)

    assert response.status_code == status.HTTP_200_OK
    print('Response JSON:', response.json())
    assert response.json() == {'access_token': 'bearer mock_access_token', 'customer_id': mock_user.id}

def test_auth_invalid_credentials(mocker):
    mock_user = None
    mocker.patch('app.services.repository.get_user_by_email', return_value=mock_user)

    form_data = {'username': 'invalid@example.com', 'password': 'wrong_password'}

    response = client.post('/token', data=form_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Nome de usuário ou senha incorretos'}
