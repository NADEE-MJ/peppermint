import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.models.transaction import TransactionCreate, TransactionUpdate
from src.tests.utils.transaction import create_test_transaction
from src.tests.utils.budget import create_test_budget
from src.tests.utils.category import create_test_category
from src.tests.utils.account import create_test_account
from src.tests.utils.user import create_random_user


@pytest.mark.asyncio
async def test_create_transaction(db: AsyncSession) -> None:
    user = await create_random_user(db)
    budget = await create_test_budget(db, user_id=user.id)
    category = await create_test_category(db, user_id=user.id, budget_id=budget.id)
    account = await create_test_account(db, user_id=user.id)
    # code from create_test_transaction copied for clarity
    transaction = TransactionCreate(
        amount=400,
        desc="test transaction",
        date="2023-05-01",
    )
    transaction_from_db = await crud.transaction.create(
        db,
        obj_in=transaction,
        category_id=category.id,
        account_id=account.id,
        budget_id=budget.id,
        user_id=user.id,
    )

    # ? deletes user and associated transactions
    await crud.user.remove(db, id=user.id)
    assert transaction_from_db
    assert transaction_from_db.user_id == user.id


@pytest.mark.asyncio
async def test_get_all_transactions_for_user(db: AsyncSession) -> None:
    user = await create_random_user(db)
    budget = await create_test_budget(db, user_id=user.id)
    category = await create_test_category(db, user_id=user.id, budget_id=budget.id)
    account = await create_test_account(db, user_id=user.id)
    await create_test_transaction(
        db, user_id=user.id, category_id=category.id, account_id=account.id, budget_id=budget.id
    )
    transactions = await crud.transaction.get_all_transactions_for_user(db, user_id=user.id)

    await crud.user.remove(db, id=user.id)
    assert len(transactions) == 1
    assert transactions[0].user_id == user.id


@pytest.mark.asyncio
async def test_get_all_transactions_for_user(db: AsyncSession) -> None:
    user = await create_random_user(db)
    budget = await create_test_budget(db, user_id=user.id)
    category = await create_test_category(db, user_id=user.id, budget_id=budget.id)
    account = await create_test_account(db, user_id=user.id)
    await create_test_transaction(
        db, user_id=user.id, category_id=category.id, account_id=account.id, budget_id=budget.id
    )
    transactions = await crud.transaction.get_all_transactions_for_user(db, user_id=user.id)

    await crud.user.remove(db, id=user.id)
    assert len(transactions) == 1
    assert transactions[0].user_id == user.id


@pytest.mark.asyncio
async def test_update_transaction(db: AsyncSession) -> None:
    user = await create_random_user(db)
    user = await create_random_user(db)
    budget = await create_test_budget(db, user_id=user.id)
    category = await create_test_category(db, user_id=user.id, budget_id=budget.id)
    account = await create_test_account(db, user_id=user.id)
    transaction_from_db = await create_test_transaction(
        db, user_id=user.id, category_id=category.id, account_id=account.id, budget_id=budget.id
    )
    transaction = TransactionUpdate(desc="updated test transaction desc")
    transaction_from_db = await crud.transaction.update(db, db_obj=transaction_from_db, obj_in=transaction)

    await crud.user.remove(db, id=user.id)
    assert transaction_from_db.desc == transaction.desc
