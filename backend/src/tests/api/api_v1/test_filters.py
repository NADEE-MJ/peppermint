import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.core.config import settings
from src.models.user import User
from src.tests.utils.budget import create_test_budget
from src.tests.utils.category import create_test_category
from src.tests.utils.filter import create_test_filter
from src.tests.utils.user import get_auth_header


@pytest.mark.asyncio
async def test_get_all_filters(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    category = await create_test_category(db, user_id=test_user.id, budget_id=budget.id)
    await create_test_filter(db, user_id=test_user.id, category_id=category.id)
    response = client.get(f"{settings.API_VERSION_STR}/filters/", headers=headers)
    filters = response.json()

    assert len(filters) == 1
    assert filters[0]["user_id"] == test_user.id


@pytest.mark.asyncio
async def test_get_filter(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    category = await create_test_category(db, user_id=test_user.id, budget_id=budget.id)
    filter = await create_test_filter(db, user_id=test_user.id, category_id=category.id)
    response = client.get(f"{settings.API_VERSION_STR}/filters/{filter.id}", headers=headers)
    filter = response.json()

    assert filter["user_id"] == test_user.id


@pytest.mark.asyncio
async def test_get_all_filters_by_category(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    category = await create_test_category(db, user_id=test_user.id, budget_id=budget.id)
    await create_test_filter(db, user_id=test_user.id, category_id=category.id)
    response = client.get(f"{settings.API_VERSION_STR}/filters/category/{category.id}", headers=headers)
    filters = response.json()

    assert len(filters) == 1
    assert filters[0]["user_id"] == test_user.id


@pytest.mark.asyncio
async def test_create_filter(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    category = await create_test_category(db, user_id=test_user.id, budget_id=budget.id)
    data = {"filter_by": "test"}
    response = client.post(f"{settings.API_VERSION_STR}/filters/category/{category.id}", headers=headers, json=data)
    filter = response.json()

    assert filter["user_id"] == test_user.id
    assert filter["filter_by"] == "test"


@pytest.mark.asyncio
async def test_update_filter(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    category = await create_test_category(db, user_id=test_user.id, budget_id=budget.id)
    filter = await create_test_filter(db, user_id=test_user.id, category_id=category.id)
    data = {"filter_by": "test new filter"}
    response = client.put(f"{settings.API_VERSION_STR}/filters/{filter.id}", headers=headers, json=data)
    filter = response.json()

    assert filter["user_id"] == test_user.id
    assert filter["filter_by"] == "test new filter"


@pytest.mark.asyncio
async def test_remove_filter(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    category = await create_test_category(db, user_id=test_user.id, budget_id=budget.id)
    filter = await create_test_filter(db, user_id=test_user.id, category_id=category.id)
    response = client.delete(f"{settings.API_VERSION_STR}/filters/{filter.id}", headers=headers)
    filter = response.json()

    assert filter["user_id"] == test_user.id

    response = client.get(f"{settings.API_VERSION_STR}/filters/", headers=headers)
    filters = response.json()

    assert len(filters) == 0
