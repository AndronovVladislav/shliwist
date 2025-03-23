from fastapi import APIRouter, Depends, status, Response, HTTPException

from src.routes.auth.validation import get_current_refresh_payload
from src.schemas.auth import UserSignupRequest, UserLoginRequest, LoggedInUserResponse
from src.services.auth import (
    signup as signup_service,
    signin as signin_service,
    refresh_token as refresh_token_service
)

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/signup')
async def signup(user_data: UserSignupRequest) -> Response:
    """
    Регистрация нового пользователя.
    """
    new_user = await signup_service(user_data)
    if new_user:
        return Response(status_code=status.HTTP_201_CREATED)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/signin')
async def signin(user_data: UserLoginRequest) -> LoggedInUserResponse:
    """
    Вход в систему. Возвращает access и refresh токены.
    """
    access, refresh = await signin_service(user_data)
    return LoggedInUserResponse(access_token=access, refresh_token=refresh)


@router.post('/refresh')
async def refresh_token(refresh_payload: dict = Depends(get_current_refresh_payload)) -> LoggedInUserResponse:
    """
    Эндпоинт для получения нового access/refresh токена по действующему refresh токену.
    """
    access, refresh = await refresh_token_service(refresh_payload)
    return LoggedInUserResponse(access_token=access, refresh_token=refresh)
