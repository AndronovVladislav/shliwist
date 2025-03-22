from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import InvalidTokenError

from src.models.user import User
from src.routes.auth.utils import (
    decode_jwt,
    TokenType,
    TOKEN_TYPE_FIELD,
    get_user_by_username
)

bearer_scheme = HTTPBearer()


def get_current_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> str:
    if credentials is None or credentials.scheme.lower() != 'bearer':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен невалиден')
    return credentials.credentials


def get_current_token_payload(token: str = Depends(get_current_token)) -> dict:
    """
    Декодирует access или refresh токен.
    """
    print(token)
    try:
        payload = decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Невалидный JWT-токен',
        ) from e

    return payload


def validate_token_type(payload: dict, expected_type: str) -> None:
    """
    Проверяет, что в декодированном токене нужный тип.
    """
    current_type = payload.get(TOKEN_TYPE_FIELD)
    if current_type != expected_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Ожидается {expected_type}-токен, получен: {current_type}',
        )


def get_current_username(payload: dict = Depends(get_current_token_payload)) -> str:
    """
    Извлекает username из access-токена.
    """
    validate_token_type(payload, TokenType.ACCESS)

    username = payload.get('sub')
    if not username:
        raise HTTPException(status_code=401, detail='Токен не содержит username')
    return username


async def get_current_user(username: str = Depends(get_current_username)) -> User:
    """
    Используется для эндпоинтов, требующих access-токен.
    """
    user = await get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Пользователь не найден',
        )

    return user


def get_current_refresh_payload(token: str = Depends(get_current_token)) -> dict:
    """
    Зависимость для эндпоинта обновления токена. Проверяет, что токен валиден.
    """
    try:
        payload = decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Невалидный JWT-токен',
        ) from e

    validate_token_type(payload, TokenType.REFRESH)
    return payload
