from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.crud.base import CRUDBase
from src.models.account import Account, AccountCreate, AccountUpdate


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):
    async def get_all_accounts_for_user(self, db: AsyncSession, *, user_id: int) -> :
        result = await db.execute(select(Account).filter(Account.user_id == user_id))
        return result.scalars().all()

    async def get_by_email(self, db: AsyncSession, *, email: str) -> list | None:
        result = await db.execute(select(Account).filter(Account.email == email))
        return result.scalars().first()

    async def account_create(self, db: AsyncSession, *, obj_in: AccountCreate) -> Account:
        db_obj = Account(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            created_at=datetime.now(),
            is_active=True,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def account_update(self, db: Any, *, db_obj: Account, obj_in: AccountUpdate | dict(str, Any)) -> Account:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data and update_data["password"] is not None :
            hashed_password = get_password_hash(update_data["password"])
            update_data["password"] = hashed_password
        else:
            del update_data["password"]
        return await super().update(db, db_obj=db_obj, obj_in=update_data)


Account = CRUDAccount(Account)
