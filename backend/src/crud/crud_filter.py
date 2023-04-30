from datetime import datetime
from math import ceil
from typing import Optional

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.crud.base import CRUDBase
from src.models.filter import Filter, FilterCreate, FilterUpdate


class CRUDFilter(CRUDBase[Filter, FilterCreate, FilterUpdate]):
    async def get_all_filters_for_user(
        self, db: AsyncSession, *, user_id: int, page: int = 0, limit: int = 10
    ) -> Optional[dict[str, int | list[Filter]]]:
        if limit == -1:
            paginated_results = (await db.execute(select(Filter).filter(Filter.user_id == user_id))).scalars().all()
            return {"paginated_results": paginated_results, "total_pages": 1}
        page *= limit

        paginated_results = (
            (await db.execute(select(Filter).filter(Filter.user_id == user_id).offset(page).limit(limit)))
            .scalars()
            .all()
        )

        count = (await db.execute(select(func.count(Filter.id)).filter(Filter.user_id == user_id))).scalars().first()
        if count is not None:
            total_pages = ceil(count / limit)
        else:
            total_pages = 0

        return {"paginated_results": paginated_results, "total_pages": total_pages}

    async def get_all_filters_for_category(
        self, db: AsyncSession, *, user_id: int, category_id: int, page: int = 0, limit: int = 10
    ) -> Optional[dict[str, int | list[Filter]]]:
        page *= limit
        paginated_results = (
            (
                await db.execute(
                    select(Filter)
                    .filter(Filter.user_id == user_id)
                    .filter(Filter.category_id == category_id)
                    .offset(page)
                    .limit(limit)
                )
            )
            .scalars()
            .all()
        )

        count = (
            (
                await db.execute(
                    select(func.count(Filter.id))
                    .filter(Filter.user_id == user_id)
                    .filter(Filter.category_id == category_id)
                )
            )
            .scalars()
            .first()
        )
        if count is not None:
            total_pages = ceil(count / limit)
        else:
            total_pages = 0

        return {"paginated_results": paginated_results, "total_pages": total_pages}

    async def create(  # type: ignore
        self, db: AsyncSession, *, obj_in: FilterCreate, user_id: int, category_id: int
    ) -> Filter:
        db_obj = Filter(filter_by=obj_in.filter_by, created_at=datetime.now(), user_id=user_id, category_id=category_id)
        return await super().create(db, obj_in=db_obj)


filter = CRUDFilter(Filter)
