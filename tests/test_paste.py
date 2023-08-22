import pytest
from httpx import AsyncClient


async def test_add_paste(ac: AsyncClient):
    response = await ac.post('/paste/', json={
        'message': 'test message',
        'lifetime': '10M',
    })

    assert response.status_code == 200

    paste_id = response.json()['data']['id']
    pytest.paste_id = paste_id


async def test_get_paste(ac: AsyncClient):
    response = await ac.get(f'/paste/{pytest.paste_id}')

    assert response.status_code == 200
    assert response.json()['data']['message'] == 'test message'


async def test_unauthorized_delete_paste(ac: AsyncClient):
    response = await ac.get(f'/paste/delete/{pytest.paste_id}')

    assert response.status_code == 401
