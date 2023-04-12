import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.models.account import AccountCreate, AccountUpdate
from src.tests.utils.account import create_test_account
from src.tests.utils.user import create_random_user


@pytest.mark.asyncio
async def test_create_account(db: AsyncSession) -> None:
    user = await create_random_user(db)

    # code from create_test_account copied for clarity
    account = AccountCreate(account_type="checking", name="test account")
    account_from_db = await crud.account.create(db, obj_in=account, user_id=user.id)

    # ? deletes user and associated accounts
    await crud.user.remove(db, id=user.id)  # type: ignore
    assert account_from_db
    assert account_from_db.user_id == user.id


@pytest.mark.asyncio
async def test_get_all_accounts_for_user(db: AsyncSession) -> None:
    user = await create_random_user(db)
    await create_test_account(db, user_id=user.id)
    accounts = await crud.account.get_all_accounts_for_user(db, user_id=user.id)

    await crud.user.remove(db, id=user.id)  # type: ignore
    assert len(accounts) == 1
    assert accounts[0].user_id == user.id


@pytest.mark.asyncio
async def test_update_account(db: AsyncSession) -> None:
    user = await create_random_user(db)
    account_from_db = await create_test_account(db, user_id=user.id)
    account = AccountUpdate(name="updated test account")
    account_from_db = await crud.account.update(db, db_obj=account_from_db, obj_in=account)

    await crud.user.remove(db, id=user.id)  # type: ignore
    assert account_from_db.name == account.name
