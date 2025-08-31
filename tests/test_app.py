from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo!'}


def test_create_user(client):
    response = client.post(  # UserSchema
        '/users/',
        json={
            'username': 'teste_username',
            'email': 'teste@teste.com',
            'password': 'senhateste',
        },
    )

    # Voltou o status_code correto?
    assert response.status_code == HTTPStatus.CREATED

    # Se sim, validar o user_public:
    assert response.json() == {
        'username': 'teste_username',
        'email': 'teste@teste.com',
        'id': 1,
    }


def test_read_user(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'teste_username',
                'email': 'teste@teste.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'teste_username2',
            'email': 'teste@teste.com',
            'password': 'senhateste',
            'id': 1,
        },
    )

    assert response.json() == {
        'username': 'teste_username2',
        'email': 'teste@teste.com',
        'id': 1,
    }


def test_delete_user(client):
    response = client.delete('users/1')

    assert response.json() == {'message': 'User deleted'}
