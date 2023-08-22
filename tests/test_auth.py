import pytest
from conftest import client
from httpx import AsyncClient


def test_register():
    response = client.post('/auth/register', json={
        'email': 'test@test.com',
        'password': 'password123',
        'username': 'user',
    })

    assert response.status_code == 201


def test_login():
    response = client.post('/auth/jwt/login', data={
        'username': 'test@test.com',
        'password': 'password123',
    })

    pytest.cookie = response.cookies

    assert response.status_code == 204


# async def test_logout(ac: AsyncClient):
#     response = await ac.post('/auth/jwt/logout', cookies=pytest.cookie)
#     assert response.status_code == 204


