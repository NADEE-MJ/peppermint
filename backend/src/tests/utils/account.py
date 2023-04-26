from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.models.account import Account, AccountCreate


async def create_test_account(db: AsyncSession, user_id: int) -> Account:
    account_create = AccountCreate(account_type="checking", name="test account")
    account = await crud.account.create(db, obj_in=account_create, user_id=user_id)

    return account
