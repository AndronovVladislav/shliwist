import uuid
from datetime import datetime, timedelta, timezone
from enum import StrEnum

import bcrypt
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.models.user import User
from src.models.utils import connection

TOKEN_TYPE_FIELD = 'token_type'


class TokenType(StrEnum):
    ACCESS = 'access'
    REFRESH = 'refresh'


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def validate_password(password: str, hashed_password: str) -> bool:
    """
    Проверяем, что пароль password совпадает с сохранённым в БД hashed_password.
    """
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password.encode() if isinstance(hashed_password, str) else hashed_password,
    )


def create_jwt(subject: str,
               token_type: str,
               expires_delta: timedelta,
               additional_claims: dict | None = None,
               ) -> str:
    """
    Универсальная функция для создания JWT.

    subject – уникальный идентификатор, который кладётся в sub
    token_type – тип токена из TokenType
    expires_delta – timedelta
    additional_claims – любые доп. поля
    """
    private_key = settings.jwt.private_key_path.read_text()
    algorithm = settings.jwt.algorithm

    now = datetime.now(tz=timezone.utc)
    expire = now + expires_delta

    payload = {
        'sub': subject,
        TOKEN_TYPE_FIELD: token_type,
        'iat': now,
        'exp': expire,
        'jti': str(uuid.uuid4()),
    }
    if additional_claims:
        payload.update(additional_claims)

    token = jwt.encode(payload, private_key, algorithm=algorithm)
    return token


def decode_jwt(token: str) -> dict:
    """
    Расшифровываем токен. Если невалиден – выбрасывается исключение.
    """
    public_key = settings.jwt.public_key_path.read_text()
    algorithm = settings.jwt.algorithm
    payload = jwt.decode(token, public_key, algorithms=[algorithm])
    return payload


def create_access_token(subject: str, additional_claims: dict | None = None) -> str:
    """
    Создаём access-токен с коротким сроком жизни.
    """
    expires_delta = timedelta(minutes=settings.jwt.access_token_expire_minutes)
    return create_jwt(
        subject=subject,
        token_type=TokenType.ACCESS,
        expires_delta=expires_delta,
        additional_claims=additional_claims,
    )


def create_refresh_token(subject: str, additional_claims: dict | None = None) -> str:
    """
    Создаём refresh-токен с более долгим сроком жизни.
    """
    expires_delta = timedelta(minutes=settings.jwt.refresh_token_expire_minutes)
    return create_jwt(
        subject=subject,
        token_type=TokenType.REFRESH,
        expires_delta=expires_delta,
        additional_claims=additional_claims,
    )


@connection
async def get_user_by_username(username: str, session: AsyncSession) -> User | None:
    """
    Ищет пользователя в БД по username.
    """
    q = select(User).where(User.username == username)
    result = await session.execute(q)
    return result.scalar_one_or_none()
