from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
from src.main import app
from src.models.user import User
from src.tests.utils.user import create_test_user


@pytest_asyncio.fixture(scope="function")
async def db() -> AsyncGenerator:
    async_engine = create_async_engine(settings.POSTGRES_DSN, echo=True, future=True)
    session = sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with session() as s:
        yield s

    await async_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_user(db: AsyncSession) -> User:
    user = await create_test_user(db)
    return user


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(app, base_url=settings.SERVER_HOST) as c:
        yield c
