from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.models.utils import connection
from src.routes.auth.utils import (
    get_user_by_username,
    hash_password,
    validate_password,
    create_access_token,
    create_refresh_token,
)
from src.schemas.auth import UserSignupRequest, UserLoginRequest


@connection
async def signup(credentials: UserSignupRequest, session: AsyncSession) -> User:
    existing_user = await get_user_by_username(credentials.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь с таким username уже существует',
        )

    new_user = User(
        username=credentials.username,
        hashed_password=hash_password(credentials.password),
    )
    session.add(new_user)
    return new_user


async def signin(credentials: UserLoginRequest) -> tuple[str, str]:
    user: User = await get_user_by_username(credentials.username)
    if not (user and validate_password(credentials.password, user.hashed_password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверные username или пароль')

    access = create_access_token(subject=user.username)
    refresh = create_refresh_token(subject=user.username)
    return access, refresh


async def refresh_token(token_payload: dict) -> tuple[str, str]:
    username = token_payload.get('sub')
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Некорректный payload токена')

    user = await get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Пользователь не найден')

    new_access_token = create_access_token(subject=user.username)
    new_refresh_token = create_refresh_token(subject=user.username)
    return new_access_token, new_refresh_token
