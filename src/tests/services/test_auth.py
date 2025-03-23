import pytest
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.services.auth import signup, signin, refresh_token
from src.schemas.auth import UserSignupRequest, UserLoginRequest


@pytest.mark.asyncio
async def test_signup_new_user(mocker):
    session = mocker.MagicMock(spec=AsyncSession)
    mocker.patch('src.services.auth.get_user_by_username', return_value=None)
    mocker.patch('src.services.auth.hash_password', return_value='hashed-pass')

    credentials = UserSignupRequest(username='newuser', password='password')
    user = await signup(credentials, session=session)

    assert isinstance(user, User)
    assert user.username == 'newuser'
    session.add.assert_called_once()


@pytest.mark.asyncio
async def test_signup_existing_user(mocker):
    session = mocker.MagicMock(spec=AsyncSession)
    mocker.patch('src.services.auth.get_user_by_username', return_value=User())

    credentials = UserSignupRequest(username='existing', password='pass')

    with pytest.raises(HTTPException) as exc_info:
        await signup(credentials, session=session)

    assert exc_info.value.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_signin_valid(mocker):
    mock_user = User(username='tester', hashed_password='hashed')
    mocker.patch('src.services.auth.get_user_by_username', return_value=mock_user)
    mocker.patch('src.services.auth.validate_password', return_value=True)
    mocker.patch('src.services.auth.create_access_token', return_value='access')
    mocker.patch('src.services.auth.create_refresh_token', return_value='refresh')

    credentials = UserLoginRequest(username='tester', password='any')
    access, refresh = await signin(credentials)

    assert access == 'access'
    assert refresh == 'refresh'


@pytest.mark.asyncio
async def test_signin_invalid_credentials(mocker):
    mocker.patch('src.services.auth.get_user_by_username', return_value=None)

    credentials = UserLoginRequest(username='invalid', password='wrong')

    with pytest.raises(HTTPException) as exc_info:
        await signin(credentials)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_refresh_token_valid(mocker):
    mocker.patch('src.services.auth.get_user_by_username', return_value=User(username='bob'))
    mocker.patch('src.services.auth.create_access_token', return_value='access123')
    mocker.patch('src.services.auth.create_refresh_token', return_value='refresh123')

    payload = {'sub': 'bob'}
    access, refresh = await refresh_token(payload)

    assert access == 'access123'
    assert refresh == 'refresh123'


@pytest.mark.asyncio
async def test_refresh_token_invalid_payload():
    with pytest.raises(HTTPException, match='') as exc_info:
        await refresh_token({})

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
