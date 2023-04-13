from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.crud.base import CRUDBase
from src.models.account import Account, AccountCreate, AccountUpdate


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):
    async def get_all_accounts_for_user(self, db: AsyncSession, *, user_id: int) -> Optional[list[Account]]:
        result = await db.execute(select(Account).filter(Account.user_id == user_id))
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: AccountCreate, user_id: int) -> Account:  # type: ignore
        db_obj = Account(name=obj_in.name, account_type=obj_in.account_type, created_at=datetime.now(), user_id=user_id)
        return await super().create(db, obj_in=db_obj)  # type: ignore


account = CRUDAccount(Account)
