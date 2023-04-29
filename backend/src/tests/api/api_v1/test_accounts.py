import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.config import settings
from src.models.user import User
from src.tests.utils.account import create_test_account
from src.tests.utils.user import get_auth_header


@pytest.mark.asyncio
async def test_get_all_accounts(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    await create_test_account(db, user_id=test_user.id)
    response = client.get(f"{settings.API_VERSION_STR}/accounts/", headers=headers)
    accounts = response.json()

    assert len(accounts) == 1
    assert accounts[0]["user_id"] == test_user.id


@pytest.mark.asyncio
async def test_get_account(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    account = await create_test_account(db, user_id=test_user.id)
    response = client.get(f"{settings.API_VERSION_STR}/accounts/{account.id}", headers=headers)
    account = response.json()

    assert account["user_id"] == test_user.id


@pytest.mark.asyncio
async def test_create_account(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    data = {"name": "test", "account_type": "checking"}
    response = client.post(f"{settings.API_VERSION_STR}/accounts/", headers=headers, json=data)
    account = response.json()

    assert account["user_id"] == test_user.id
    assert account["name"] == "test"


@pytest.mark.asyncio
async def test_update_account(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    account = await create_test_account(db, user_id=test_user.id)
    data = {"name": "test_new"}
    response = client.put(f"{settings.API_VERSION_STR}/accounts/{account.id}", headers=headers, json=data)
    account = response.json()

    assert account["user_id"] == test_user.id
    assert account["name"] == "test_new"


@pytest.mark.asyncio
async def test_remove_account(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    account = await create_test_account(db, user_id=test_user.id)
    response = client.delete(f"{settings.API_VERSION_STR}/accounts/{account.id}", headers=headers)
    account = response.json()

    assert account["user_id"] == test_user.id

    response = client.get(f"{settings.API_VERSION_STR}/accounts/", headers=headers)
    accounts = response.json()

    assert len(accounts) == 0
