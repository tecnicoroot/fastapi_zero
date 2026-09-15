from http import HTTPStatus

import pytest
from jwt import decode

from fastapi_zero.security import create_access_token
from fastapi_zero.settings import Settings

settings = Settings()


@pytest.mark.asyncio
async def test_jwt_token_creation():
    data = {'teste': 'teste'}

    token = create_access_token(data)

    decoded = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decoded['teste'] == data['teste']
    assert 'exp' in decoded


@pytest.mark.asyncio
async def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer invalid_token'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


@pytest.mark.asyncio
async def test_jwt_user_not_found(client):
    token = create_access_token(
        data={'sub': 'usuario.inexistente@example.com'}
    )
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


@pytest.mark.asyncio
async def test_jwt_email_empty(client):
    token = create_access_token(data={'sub': ''})
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
