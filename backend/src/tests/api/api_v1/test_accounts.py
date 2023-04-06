import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.core.config import settings
from src.models.user import User
from src.tests.utils.user import TEST_USER_EMAIL, get_auth_header
from src.tests.utils.account import create_test_account


@pytest.mark.asyncio
async def test_get_all_accounts(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    await create_test_account(db, user_id=test_user.id)
    response = client.get(f"{settings.API_VERSION_STR}/accounts/", headers=headers)
    accounts = response.json()
    await crud.user.remove(db, id=test_user.id)  # type: ignore

    assert len(accounts) == 1
    assert accounts[0]["user_id"] == test_user.id


@pytest.mark.asyncio
async def test_get_account(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    await create_test_account(db, user_id=test_user.id)
    response = client.get(f"{settings.API_VERSION_STR}/accounts/", headers=headers)
    accounts = response.json()
    await crud.user.remove(db, id=test_user.id)  # type: ignore

    assert len(accounts) == 1
    assert accounts[0]["user_id"] == test_user.id
