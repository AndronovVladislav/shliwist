import pytest
from fastapi import HTTPException

from src.models import User
from src.routes.auth.utils import TokenType
from src.routes.auth.validation import (
    get_current_token_payload,
    validate_token_type,
    get_current_user,
    get_current_refresh_payload
)


@pytest.fixture
def invalid_token() -> str:
    """Создаёт невалидный токен"""
    return 'invalid.token.payload'


@pytest.mark.asyncio
async def test_get_current_auth_user(mocker, user_1: User):
    """Тестирует получение пользователя по access-токену"""
    mocker.patch('src.routes.auth.validation.get_user_by_username', return_value=user_1)

    user = await get_current_user()
    assert user.username == 'test_user_1'


@pytest.mark.asyncio
async def test_get_current_auth_user_not_found(mocker):
    """Тестирует случай, когда пользователь не найден"""
    mocker.patch('src.routes.auth.validation.get_user_by_username', return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user()
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == 'Пользователь не найден'


@pytest.mark.parametrize('token_type', [TokenType.ACCESS, TokenType.REFRESH])
def test_validate_token_type(token_type):
    """Проверяет, что функция валидирует правильный тип токена и выбрасывает ошибку для неправильного"""
    payload = {'token_type': token_type}
    validate_token_type(payload, token_type)

    with pytest.raises(HTTPException) as exc_info:
        validate_token_type(payload, TokenType.ACCESS if token_type == TokenType.REFRESH else TokenType.REFRESH)

    assert exc_info.value.status_code == 401


@pytest.mark.parametrize(
    'token_fixture, expected_type',
    [
        ('access_token', TokenType.ACCESS),
        ('refresh_token', TokenType.REFRESH)
    ],
)
def test_get_current_token_payload(token_fixture, expected_type, request):
    """Тестирует декодирование валидных токенов (и access, и refresh)"""
    token = request.getfixturevalue(token_fixture)
    payload = get_current_token_payload(token)

    assert payload['sub'] == 'test_user_1'
    assert payload['token_type'] == expected_type


@pytest.mark.parametrize(
    'token_fixture, expected_status, expected_detail',
    [
        ('invalid_token', 401, 'Невалидный JWT-токен'),
    ],
)
def test_get_current_token_payload_invalid(token_fixture, expected_status, expected_detail, request):
    """Тестирует обработку невалидных токенов"""
    token = request.getfixturevalue(token_fixture)

    with pytest.raises(HTTPException) as exc_info:
        get_current_token_payload(token)

    assert exc_info.value.status_code == expected_status
    assert exc_info.value.detail == expected_detail


@pytest.mark.parametrize(
    'token_fixture, expected_type',
    [
        ('refresh_token', TokenType.REFRESH)
    ],
)
def test_get_current_refresh_payload(token_fixture, expected_type, request):
    """Тестирует валидацию refresh-токена"""
    token = request.getfixturevalue(token_fixture)
    payload = get_current_refresh_payload(token)

    assert payload['sub'] == 'test_user_1'
    assert payload['token_type'] == expected_type


@pytest.mark.parametrize(
    'token_fixture, expected_status, expected_detail',
    [
        ('invalid_token', 401, 'Невалидный JWT-токен'),
    ],
)
def test_get_current_refresh_payload_invalid(token_fixture, expected_status, expected_detail, request):
    """Тестирует обработку невалидного refresh-токена"""
    token = request.getfixturevalue(token_fixture)

    with pytest.raises(HTTPException) as exc_info:
        get_current_refresh_payload(token)

    assert exc_info.value.status_code == expected_status
    assert exc_info.value.detail == expected_detail
