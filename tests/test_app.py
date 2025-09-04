from http import HTTPStatus

from fast_zero_rbe.schemas import UserPublic


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


def test_read_users(client):

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
        ]
    }


def test_read_users_with_users(client, user):

    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [user_schema]
    }


def test_update_user(client, user):
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


def test_delete_user(client, user):
    response = client.delete('users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_update_integrity_error(client, user):

    client.post(
        '/users/',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret'
        }
    )

    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword'
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Username or Email already exists'
    }
