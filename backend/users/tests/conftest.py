import os

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from backend.config import settings
from backend.main import backend

pytest.register_assert_rewrite('tests.e2e.api_client')
os.environ['TESTING'] = 'True'


@pytest.fixture
async def async_client_api():
    base_url = settings.TEST_URL + settings.DEFAULT_URL_PREFIX_V1
    async with AsyncClient(
        transport=ASGITransport(app=backend),
        base_url=base_url,
    ) as async_client:
        yield async_client


@pytest.fixture
async def postgres_db():
    engine = create_async_engine(
        settings.get_database_url,
        isolation_level="SERIALIZABLE",
        echo=False,
        poolclass=NullPool,
    )

    return engine


@pytest.fixture
async def postgres_session_factory(postgres_db):
    async_session = sessionmaker(
        bind=postgres_db,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session


@pytest.fixture
async def session(postgres_session_factory):
    return postgres_session_factory
