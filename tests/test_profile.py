from httpx import AsyncClient


async def test_get_profile(ac: AsyncClient):
    response = await ac.get(f'/profile/1')

    assert response.status_code == 200
