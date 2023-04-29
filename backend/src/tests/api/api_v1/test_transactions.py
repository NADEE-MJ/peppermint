import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.core.config import settings
from src.models.user import User
from src.tests.utils.account import create_test_account
from src.tests.utils.budget import create_test_budget
from src.tests.utils.category import create_test_category
from src.tests.utils.filter import create_parser_test_filters
from src.tests.utils.transaction import (
    TRANSACTIONS_TO_PARSE_BASE64,
    create_test_transaction,
)
from src.tests.utils.user import get_auth_header


@pytest.mark.asyncio
async def test_get_all_transactions(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    category = await create_test_category(db, user_id=test_user.id, budget_id=budget.id)
    account = await create_test_account(db, user_id=test_user.id)
    await create_test_transaction(
        db, user_id=test_user.id, category_id=category.id, account_id=account.id, budget_id=budget.id
    )
    response = client.get(f"{settings.API_VERSION_STR}/transactions/", headers=headers)
    transactions = response.json()

    assert len(transactions) == 1
    assert transactions[0]["user_id"] == test_user.id


@pytest.mark.asyncio
async def test_get_transaction(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    category = await create_test_category(db, user_id=test_user.id, budget_id=budget.id)
    account = await create_test_account(db, user_id=test_user.id)
    transaction = await create_test_transaction(
        db, user_id=test_user.id, category_id=category.id, account_id=account.id, budget_id=budget.id
    )
    response = client.get(f"{settings.API_VERSION_STR}/transactions/{transaction.id}", headers=headers)
    transaction = response.json()

    assert transaction["user_id"] == test_user.id


@pytest.mark.asyncio
async def test_get_all_transactions_by_account(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    category = await create_test_category(db, user_id=test_user.id, budget_id=budget.id)
    account = await create_test_account(db, user_id=test_user.id)
    await create_test_transaction(
        db, user_id=test_user.id, category_id=category.id, account_id=account.id, budget_id=budget.id
    )
    response = client.get(f"{settings.API_VERSION_STR}/transactions/account/{account.id}", headers=headers)
    transactions = response.json()

    assert len(transactions) == 1
    assert transactions[0]["user_id"] == test_user.id


@pytest.mark.asyncio
async def test_get_all_transactions_by_budget_and_category(
    db: AsyncSession, client: TestClient, test_user: User
) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    category = await create_test_category(db, user_id=test_user.id, budget_id=budget.id)
    account = await create_test_account(db, user_id=test_user.id)
    await create_test_transaction(
        db, user_id=test_user.id, category_id=category.id, account_id=account.id, budget_id=budget.id
    )
    response = client.get(
        f"{settings.API_VERSION_STR}/transactions/budget/{budget.id}/category/{category.id}", headers=headers
    )
    transactions = response.json()

    assert len(transactions) == 1
    assert transactions[0]["user_id"] == test_user.id


@pytest.mark.asyncio
async def test_get_all_transactions_by_account_and_category(
    db: AsyncSession, client: TestClient, test_user: User
) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    category = await create_test_category(db, user_id=test_user.id, budget_id=budget.id)
    account = await create_test_account(db, user_id=test_user.id)
    await create_test_transaction(
        db, user_id=test_user.id, category_id=category.id, account_id=account.id, budget_id=budget.id
    )
    response = client.get(
        f"{settings.API_VERSION_STR}/transactions/account/{account.id}/category/{category.id}", headers=headers
    )
    transactions = response.json()

    assert len(transactions) == 1
    assert transactions[0]["user_id"] == test_user.id


@pytest.mark.asyncio
async def test_create_transaction(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    category = await create_test_category(db, user_id=test_user.id, budget_id=budget.id)
    account = await create_test_account(db, user_id=test_user.id)
    data = {"desc": "test", "amount": 100, "date": "01/01/2020"}
    response = client.post(
        f"{settings.API_VERSION_STR}/transactions/budget/{budget.id}/category/{category.id}/account/{account.id}",
        headers=headers,
        json=data,
    )
    transaction = response.json()

    assert transaction["user_id"] == test_user.id
    assert transaction["desc"] == "test"


@pytest.mark.asyncio
async def test_update_transaction(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    category = await create_test_category(db, user_id=test_user.id, budget_id=budget.id)
    account = await create_test_account(db, user_id=test_user.id)
    transaction = await create_test_transaction(
        db, user_id=test_user.id, category_id=category.id, account_id=account.id, budget_id=budget.id
    )
    data = {"desc": "test new desc"}
    response = client.put(f"{settings.API_VERSION_STR}/transactions/{transaction.id}", headers=headers, json=data)
    transaction = response.json()

    assert transaction["user_id"] == test_user.id
    assert transaction["desc"] == "test new desc"


@pytest.mark.asyncio
async def test_remove_transaction(db: AsyncSession, client: TestClient, test_user: User) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    category = await create_test_category(db, user_id=test_user.id, budget_id=budget.id)
    account = await create_test_account(db, user_id=test_user.id)
    transaction = await create_test_transaction(
        db, user_id=test_user.id, category_id=category.id, account_id=account.id, budget_id=budget.id
    )
    response = client.delete(f"{settings.API_VERSION_STR}/transactions/{transaction.id}", headers=headers)
    transaction = response.json()

    assert transaction["user_id"] == test_user.id

    response = client.get(f"{settings.API_VERSION_STR}/transactions/", headers=headers)
    transactions = response.json()

    assert len(transactions) == 0


@pytest.mark.asyncio
async def test_parse_transactions_from_csv_with_no_categories(
    db: AsyncSession, client: TestClient, test_user: User
) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    account = await create_test_account(db, user_id=test_user.id)
    await create_parser_test_filters(db, user_id=test_user.id, budget_id=budget.id)

    mapping = {"Date": "date", "Description": "desc", "Amount": "amnt"}
    data = {"file": TRANSACTIONS_TO_PARSE_BASE64, "mapping": mapping}

    response = client.post(
        f"{settings.API_VERSION_STR}/transactions/parse/budget/{budget.id}/account/{account.id}",
        headers=headers,
        json=data,
    )

    res = response.json()
    assert res["success"] is True

    response = client.get(f"{settings.API_VERSION_STR}/transactions/", headers=headers)
    transactions = response.json()

    assert len(transactions) == 21


@pytest.mark.asyncio
async def test_parse_transactions_from_csv_with_categories(
    db: AsyncSession, client: TestClient, test_user: User
) -> None:
    headers = get_auth_header(client)
    budget = await create_test_budget(db, user_id=test_user.id)
    account = await create_test_account(db, user_id=test_user.id)
    await create_parser_test_filters(db, user_id=test_user.id, budget_id=budget.id)

    mapping = {"Date": "date", "Description": "desc", "Amount": "amnt", "Category": "category"}
    data = {"file": TRANSACTIONS_TO_PARSE_BASE64, "mapping": mapping}

    response = client.post(
        f"{settings.API_VERSION_STR}/transactions/parse/budget/{budget.id}/account/{account.id}",
        headers=headers,
        json=data,
    )

    res = response.json()
    assert res["success"] is True

    response = client.get(f"{settings.API_VERSION_STR}/transactions/", headers=headers)
    transactions = response.json()

    assert len(transactions) == 21
