from typing import AsyncIterator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport
from httpx import AsyncClient
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import settings
from src.main import app as fastapi_app
from src.models import User
from src.models.utils import connection
from src.models.utils import db_helper
from src.routes.auth.utils import hash_password

engine = create_async_engine(
    url=settings.db.url,
    echo=True,
    echo_pool=True,
    poolclass=NullPool,
)


@pytest.fixture(scope='session')
async def app() -> FastAPI:
    return fastapi_app


@pytest.fixture(scope='session')
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client


@pytest.fixture(autouse=True)
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


@pytest.fixture
async def test_user() -> User:
    """Создаёт тестового пользователя в БД перед тестом"""

    @connection
    async def create_user(session: AsyncSession) -> User:
        user = User(
            username='test_user',
            hashed_password=hash_password('test_password'),
        )
        session.add(user)
        return user

    return await create_user()
