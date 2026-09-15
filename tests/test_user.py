from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'david',
            'email': 'david@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'david',
        'email': 'david@example.com',
    }


# def test_read_users(client, token):
#    response = client.get(
#        '/users/',
#        headers={'Authorization': f'Bearer {token}'},
#        )
#

#    assert response.status_code == HTTPStatus.OK
#    assert response.json() == {'users': []}


def test_read_users_with_user(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):

    response = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'david_updated',
            'email': 'david_updated@example.com',
            'password': 'new_secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'david_updated',
        'email': 'david_updated@example.com',
    }


def test_update_user_not_found(client, token):
    response = client.put(
        '/users/2',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'david_updated',
            'email': 'david_updated@example.com',
            'password': 'new_secret',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user(client, user, token):
    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted successfully'}


def test_delete_user_not_found(client, token):
    response = client.delete(
        '/users/2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_integrity_erro(client, user, token):
    client.post(
        '/users',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'zeca',
            'email': 'zeca@example.com',
            'password': 'secret',
        },
    )
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'zeca',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_create_user_username_integrity_error(client, user):
    client.post(
        '/users',
        json={
            'username': 'teste2',
            'email': 'teste2@teste.com',
            'password': 'testtest',
        },
    )

    response = client.post(
        '/users',
        json={
            'username': 'teste2',
            'email': 'teste3@teste.com',
            'password': 'testtest',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already registered'}


def test_create_user_email_integrity_error(client, user):
    client.post(
        '/users',
        json={
            'username': 'teste2',
            'email': 'teste2@teste.com',
            'password': 'testtest',
        },
    )

    response = client.post(
        '/users',
        json={
            'username': 'teste3',
            'email': 'teste2@teste.com',
            'password': 'testtest',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already registered'}


def test_create_user_put_integrity_error(client, user, token):
    client.post(
        '/users',
        json={
            'username': 'teste4',
            'email': 'teste4@teste.com',
            'password': 'testtest',
        },
    )

    response = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'teste',
            'email': 'teste4@teste.com',
            'password': 'testtest',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Username or Email already registered'
    }
