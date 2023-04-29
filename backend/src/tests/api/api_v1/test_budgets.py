import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.core.config import settings
from src.models.user import User
from src.tests.utils.budget import create_test_budget
from src.tests.utils.user import get_auth_header


@pytest.mark.asyncio
async def test_get_all_budgets(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    await create_test_budget(db, user_id=test_user.id)
    response = client.get(f"{settings.API_VERSION_STR}/budgets/", headers=headers)
    budgets = response.json()

    assert len(budgets) == 1
    assert budgets[0]["user_id"] == test_user.id


@pytest.mark.asyncio
async def test_get_budget(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    response = client.get(f"{settings.API_VERSION_STR}/budgets/{budget.id}", headers=headers)
    budget = response.json()

    assert budget["user_id"] == test_user.id


@pytest.mark.asyncio
async def test_create_budget(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    data = {"name": "test", "amount": 400}
    response = client.post(f"{settings.API_VERSION_STR}/budgets/", headers=headers, json=data)
    budget = response.json()
    category = await crud.category.get_unsorted_category_for_budget(db, user_id=test_user.id, budget_id=budget["id"])

    assert category is not None
    assert category.name == "Unsorted"
    assert budget["user_id"] == test_user.id
    assert budget["name"] == "test"


@pytest.mark.asyncio
async def test_update_budget(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    data = {"name": "test_new"}
    response = client.put(f"{settings.API_VERSION_STR}/budgets/{budget.id}", headers=headers, json=data)
    budget = response.json()

    assert budget["user_id"] == test_user.id
    assert budget["name"] == "test_new"


@pytest.mark.asyncio
async def test_remove_budget(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    response = client.delete(f"{settings.API_VERSION_STR}/budgets/{budget.id}", headers=headers)
    budget = response.json()

    assert budget["user_id"] == test_user.id

    response = client.get(f"{settings.API_VERSION_STR}/budgets/", headers=headers)
    budgets = response.json()

    assert len(budgets) == 0
