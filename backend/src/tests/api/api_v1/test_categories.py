import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.config import settings
from src.models.user import User
from src.tests.utils.budget import create_test_budget
from src.tests.utils.category import create_test_category
from src.tests.utils.user import get_auth_header


@pytest.mark.asyncio
async def test_get_all_categories(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    await create_test_category(db, user_id=test_user.id, budget_id=budget.id)
    response = client.get(f"{settings.API_VERSION_STR}/categories/", headers=headers)
    data = response.json()
    categories = data["paginated_results"]
    total_pages = data["total_pages"]

    assert len(categories) == 2
    assert total_pages == 1
    assert categories[0]["user_id"] == test_user.id


@pytest.mark.asyncio
async def test_get_category(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    category = await create_test_category(db, user_id=test_user.id, budget_id=budget.id)
    response = client.get(f"{settings.API_VERSION_STR}/categories/{category.id}", headers=headers)
    category = response.json()

    assert category["user_id"] == test_user.id


@pytest.mark.asyncio
async def test_get_all_categories_by_budget(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    await create_test_category(db, user_id=test_user.id, budget_id=budget.id)
    response = client.get(f"{settings.API_VERSION_STR}/categories/budget/{budget.id}", headers=headers)
    categories = response.json()

    assert len(categories) == 2
    assert categories[0]["user_id"] == test_user.id


@pytest.mark.asyncio
async def test_create_category(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    data = {"name": "test", "desc": "test desc", "amount": 100}
    response = client.post(f"{settings.API_VERSION_STR}/categories/budget/{budget.id}", headers=headers, json=data)
    category = response.json()

    assert category["user_id"] == test_user.id
    assert category["name"] == "test"


@pytest.mark.asyncio
async def test_update_category(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    category = await create_test_category(db, user_id=test_user.id, budget_id=budget.id)
    data = {"desc": "test new desc"}
    response = client.put(f"{settings.API_VERSION_STR}/categories/{category.id}", headers=headers, json=data)
    category = response.json()

    assert category["user_id"] == test_user.id
    assert category["desc"] == "test new desc"


@pytest.mark.asyncio
async def test_remove_category(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    category = await create_test_category(db, user_id=test_user.id, budget_id=budget.id)
    response = client.delete(f"{settings.API_VERSION_STR}/categories/{category.id}", headers=headers)
    category = response.json()

    assert category["user_id"] == test_user.id

    response = client.get(f"{settings.API_VERSION_STR}/categories/", headers=headers)
    data = response.json()
    categories = data["paginated_results"]

    assert len(categories) == 1
