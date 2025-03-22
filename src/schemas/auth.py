from pydantic import BaseModel, Field


class UserSignupRequest(BaseModel):
    """
    Схема запроса создания нового пользователя.
    """
    username: str = Field(description='Уникальное имя пользователя')
    password: str


class UserLoginRequest(BaseModel):
    """
    Схема запроса входа существующего пользователя.
    """
    username: str = Field(description='Электронная почта')
    password: str = Field(description='Пароль пользователя')


class LoggedInUserResponse(BaseModel):
    """
    Схема ответа с данными пользователя авторизовавшемуся клиенту.
    """
    access_token: str = Field(description='Токен для доступа к ресурсам системы')
    refresh_token: str = Field(description='Токен, в течение жизни которого возможно получить access-токен')
