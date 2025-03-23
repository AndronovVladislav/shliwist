import pytest


@pytest.fixture
def user_data() -> dict:
    return {
        'username': 'test-user',
        'password': 'test-password',
    }


@pytest.mark.asyncio
async def test_auth_signup(client, user_data: dict):
    response = await client.post('/auth/signup', json=user_data)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_auth_signin(client, user_data: dict):
    await client.post('/auth/signup', json=user_data)

    response = await client.post('/auth/signin', json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data
    assert 'refresh_token' in data


@pytest.mark.asyncio
async def test_auth_refresh(client, user_data: dict):
    await client.post('/auth/signup', json=user_data)
    refresh_token = (await client.post('/auth/signin', json=user_data)).json()['refresh_token']

    headers = {'Authorization': f'Bearer {refresh_token}'}
    refresh_response = await client.post('/auth/refresh', headers=headers)
    assert refresh_response.status_code == 200
    data = refresh_response.json()
    assert 'access_token' in data
    assert 'refresh_token' in data
