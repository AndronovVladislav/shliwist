from datetime import timedelta
from typing import AsyncIterator, Iterator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport
from httpx import AsyncClient
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import settings
from src.main import app as fastapi_app
from src.models import User
from src.models import WishlistItem
from src.models.utils import connection
from src.models.utils import db_helper
from src.routes.auth.utils import TokenType, create_jwt
from src.routes.auth.utils import hash_password

engine = create_async_engine(
    url=settings.db.url,
    echo=True,
    echo_pool=True,
    poolclass=NullPool,
)


@pytest.fixture(scope='session')
def app() -> FastAPI:
    return fastapi_app


@pytest_asyncio.fixture(scope='session')
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client


@pytest_asyncio.fixture(autouse=True)
async def override_db_helper():
    """Подменяет сессию в db_helper, чтобы тесты работали корректно."""
    db_helper.session_factory = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    yield

    @connection
    async def truncate_all_tables(session: AsyncSession) -> None:
        await session.execute(text('''
            DO $$ 
            DECLARE 
                r RECORD;
            BEGIN
                SET session_replication_role = 'replica';
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                    EXECUTE 'TRUNCATE TABLE ' || quote_ident(r.tablename) || ' RESTART IDENTITY CASCADE';
                END LOOP;
                SET session_replication_role = 'origin';
            END $$;
        '''))

    await truncate_all_tables()


@pytest.fixture(autouse=True)
def authorize_user(client: AsyncClient, access_token: str) -> Iterator[None]:
    original_headers = client.headers
    client.headers.update({'Authorization': f'Bearer {access_token}'})
    yield
    client.headers = original_headers


@connection
async def create_user(username: str, session: AsyncSession) -> User:
    """Создаёт тестового пользователя в БД"""
    user = User(
        username=username,
        hashed_password=hash_password('test_password'),
    )
    session.add(user)
    return user


@connection
async def create_wishlist_item(title: str, acceptor: int, donor: int, session: AsyncSession) -> WishlistItem:
    """Создаёт тестовый элемент вишлиста в БД"""
    wishlist_item = WishlistItem(
        title=title,
        price=1.0,
        link=f'https://{title}.com',
        description=f'desc_{title}',
        acceptor_id=acceptor,
        donor_id=donor,
    )
    session.add(wishlist_item)
    return wishlist_item


@pytest_asyncio.fixture
async def user_1() -> User:
    return await create_user('test_user_1')


@pytest_asyncio.fixture
async def user_2() -> User:
    return await create_user('test_user_2')


@pytest_asyncio.fixture
async def wishlist_item_1(user_1: User, user_2: User) -> WishlistItem:
    return await create_wishlist_item('item1', user_1.id, user_2.id)


@pytest_asyncio.fixture
async def wishlist_item_2(user_2: User) -> WishlistItem:
    return await create_wishlist_item('item2', user_2.id, None)


@pytest.fixture
def access_token(user_1: User) -> str:
    """Создаёт валидный access-токен"""
    return create_jwt(user_1.username, TokenType.ACCESS, timedelta(minutes=5))


@pytest.fixture
def refresh_token(user_1: User) -> str:
    """Создаёт валидный refresh-токен"""
    return create_jwt(user_1.username, TokenType.REFRESH, timedelta(minutes=15))
