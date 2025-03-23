from datetime import timedelta, datetime, timezone

import bcrypt
import pytest

from src.routes.auth.utils import (
    hash_password,
    validate_password,
    create_jwt,
    decode_jwt,
    create_access_token,
    create_refresh_token,
    get_user_by_username,
    TokenType,
)


@pytest.mark.asyncio
async def test_get_user_by_username():
    """Тестирует получение пользователя по имени"""
    user = await get_user_by_username("test_user")
    assert user is None


@pytest.mark.parametrize("password", ["securepassword", "anotherpassword"])
def test_hash_password(password):
    """Тестирует хеширование пароля"""
    hashed = hash_password(password)

    assert isinstance(hashed, str)
    assert bcrypt.checkpw(password.encode(), hashed.encode())


@pytest.mark.parametrize("password, expected", [
    ("securepassword", True),
    ("wrongpassword", False)
])
def test_validate_password(password, expected):
    """Тестирует проверку пароля"""
    hashed = hash_password("securepassword")

    assert validate_password(password, hashed) == expected


@pytest.mark.parametrize("token_type, expires_delta", [
    (TokenType.ACCESS, timedelta(minutes=15)),
    (TokenType.REFRESH, timedelta(days=7))
])
def test_create_jwt(token_type, expires_delta):
    """Тестирует создание JWT"""
    token = create_jwt("test_user", token_type, expires_delta)
    assert isinstance(token, str)

    decoded = decode_jwt(token)
    assert decoded["sub"] == "test_user"
    assert decoded["token_type"] == token_type


@pytest.mark.parametrize("create_token_func, token_type", [
    (create_access_token, TokenType.ACCESS),
    (create_refresh_token, TokenType.REFRESH)
])
def test_create_access_refresh_tokens(create_token_func, token_type):
    """Тестирует создание access и refresh токенов"""
    token = create_token_func("test_user")
    decoded = decode_jwt(token)

    assert decoded["sub"] == "test_user"
    assert decoded["token_type"] == token_type
    assert decoded["exp"] > datetime.now(timezone.utc).timestamp()
