from http import HTTPStatus


def test_get_token(client, user):
    # Como é um form_data mandaremos um "data" no lugar de "json"
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
