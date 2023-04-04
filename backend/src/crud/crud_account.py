from datetime import datetime
from typing import Optional, Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.crud.base import CRUDBase
from src.models.account import Account, AccountCreate, AccountUpdate


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):
    async def get_all_accounts_for_user(self, db: AsyncSession, *, user_id: int) -> Optional[list[Account]]:
        result = await db.execute(select(Account).filter(Account.user_id == user_id))
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: AccountCreate) -> Account:
        db_obj = Account(
            name=obj_in.name, account_type=obj_in.account_type, created_at=datetime.now(), user_id=obj_in.user_id
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: Any, *, db_obj: Account, obj_in: AccountUpdate | Dict[str, Any]) -> Account:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return await super().update(db, db_obj=db_obj, obj_in=update_data)


account = CRUDAccount(Account)
