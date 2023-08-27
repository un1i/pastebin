import pytest
from conftest import client
from httpx import AsyncClient
from fastapi_users.router import ErrorCode


def test_register():
    response = client.post('/auth/register', json={
        'email': 'test@test.com',
        'password': 'password123',
        'username': 'user',
    })

    assert response.status_code == 201


def test_user_exist_register():
    response = client.post('/auth/register', json={
        'email': 'test@test.com',
        'password': 'password123',
        'username': 'user',
    })

    assert response.status_code == 400
    detail = response.json()['detail']
    assert detail == ErrorCode.REGISTER_USER_ALREADY_EXISTS


def test_login():
    response = client.post('/auth/jwt/login', data={
        'username': 'test@test.com',
        'password': 'password123',
    })

    key = 'user_auth'
    cookie = {key: response.cookies.get(key)}
    pytest.cookie = cookie

    assert response.status_code == 204


def test_wrong_password_login():
    response = client.post('auth/jwt/login', data={
        'username': 'test@test.com',
        'password': 'password',
    })

    assert response.status_code == 400
    detail = response.json()['detail']
    assert detail == ErrorCode.LOGIN_BAD_CREDENTIALS


def test_wrong_email_login():
    response = client.post('auth/jwt/login', data={
        'username': 'test@test.net',
        'password': 'password123',
    })

    assert response.status_code == 400
    detail = response.json()['detail']
    assert detail == ErrorCode.LOGIN_BAD_CREDENTIALS


async def test_logout(ac: AsyncClient):
    response = await ac.post('/auth/jwt/logout', cookies=pytest.cookie)
    assert response.status_code == 204


async def test_unauthorized_logout(ac: AsyncClient):
    response = await ac.post('/auth/jwt/logout')

    assert response.status_code == 401
    detail = response.json()['detail']
    assert detail == 'Unauthorized'


