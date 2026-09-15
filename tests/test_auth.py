from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_non_existent_email(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': 'non-existent@domain.com',
            'password': user.clean_password,
        },
    )

    token = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert token['detail'] == 'Incorrect email or password'


def test_non_existent_password(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': 'non-existent-password',
        },
    )

    token = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert token['detail'] == 'Incorrect email or password'
