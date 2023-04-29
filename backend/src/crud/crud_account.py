from datetime import datetime
from math import ceil
from typing import Optional

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.crud.base import CRUDBase
from src.models.account import Account, AccountCreate, AccountUpdate


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):
    async def get_all_accounts_for_user(
        self, db: AsyncSession, *, user_id: int, page: int = 0, limit: int = 10
    ) -> Optional[dict[str, int | list[Account]]]:
        if limit == -1:
            paginated_results = (await db.execute(select(Account).filter(Account.user_id == user_id))).scalars().all()
            return {"paginated_results": paginated_results, "total_pages": 1}
        page *= limit
        paginated_results = (
            (await db.execute(select(Account).filter(Account.user_id == user_id).offset(page).limit(limit)))
            .scalars()
            .all()
        )

        count = (await db.execute(select(func.count(Account.id)).filter(Account.user_id == user_id))).scalars().first()
        if count is not None:
            total_pages = ceil(count / limit)
        else:
            total_pages = 0

        return {"paginated_results": paginated_results, "total_pages": total_pages}

    async def create(self, db: AsyncSession, *, obj_in: AccountCreate, user_id: int) -> Account:  # type: ignore
        db_obj = Account(name=obj_in.name, account_type=obj_in.account_type, created_at=datetime.now(), user_id=user_id)
        return await super().create(db, obj_in=db_obj)


account = CRUDAccount(Account)
