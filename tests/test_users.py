from dataclasses import asdict
from http import HTTPStatus

from sqlalchemy import select

from fast_zero_rbe.models import User
from fast_zero_rbe.schemas import UserPublic


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='test', email='test@test.com', password='secret'
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        user = session.scalar(select(User).where(User.username == 'test'))

        assert asdict(user) == {
            'id': 1,
            'username': 'test',
            'email': 'test@test.com',
            'password': 'secret',
            'created_at': time,
        }


def test_read_users(client, user, token):
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


def test_delete_user(client, user, token):
    response = client.delete(
        f'users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_update_integrity_error(client, user, token):
    client.post(
        '/users/',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}
