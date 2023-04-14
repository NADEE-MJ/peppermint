from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.crud.base import CRUDBase
from src.models.filter import Filter, FilterCreate, FilterUpdate


class CRUDFilter(CRUDBase[Filter, FilterCreate, FilterUpdate]):
    async def get_all_filters_for_user(self, db: AsyncSession, *, user_id: int) -> Optional[list[Filter]]:
        result = await db.execute(select(Filter).filter(Filter.user_id == user_id))
        return result.scalars().all()

    async def get_all_filters_for_category(
        self, db: AsyncSession, *, user_id: int, category_id: int
    ) -> Optional[list[Filter]]:
        result = await db.execute(
            select(Filter).filter(Filter.user_id == user_id).filter(Filter.category_id == category_id)
        )
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: FilterCreate, user_id: int, category_id: int) -> Filter:  # type: ignore
        db_obj = Filter(filter_by=obj_in.filter_by, created_at=datetime.now(), user_id=user_id, category_id=category_id)
        return await super().create(db, obj_in=db_obj)  # type: ignore


filter = CRUDFilter(Filter)