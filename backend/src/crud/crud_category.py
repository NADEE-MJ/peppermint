from datetime import datetime
from math import ceil
from typing import Optional

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.crud.base import CRUDBase
from src.models.category import Category, CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    async def get_all_categories_for_user(
        self, db: AsyncSession, *, user_id: int, page: int = 0, limit: int = 10
    ) -> Optional[dict[str, int | list[Category]]]:
        if limit == -1:
            paginated_results = (await db.execute(select(Category).filter(Category.user_id == user_id))).scalars().all()
            return {"paginated_results": paginated_results, "total_pages": 1}
        page *= limit
        paginated_results = (
            (await db.execute(select(Category).filter(Category.user_id == user_id).offset(page).limit(limit)))
            .scalars()
            .all()
        )

        count = (
            (await db.execute(select(func.count(Category.id)).filter(Category.user_id == user_id))).scalars().first()
        )
        if count is not None:
            total_pages = ceil(count / limit)
        else:
            total_pages = 0

        return {"paginated_results": paginated_results, "total_pages": total_pages}

    async def get_all_categories_for_budget(
        self, db: AsyncSession, *, user_id: int, budget_id: int
    ) -> Optional[list[Category]]:
        result = await db.execute(
            select(Category).filter(Category.user_id == user_id).filter(Category.budget_id == budget_id)
        )
        return result.scalars().all()

    async def get_unsorted_category_for_budget(
        self, db: AsyncSession, *, user_id: int, budget_id: int
    ) -> Optional[Category]:
        result = await db.execute(
            select(Category)
            .filter(Category.user_id == user_id)
            .filter(Category.budget_id == budget_id)
            .filter(Category.name == "Unsorted")
        )
        return result.scalars().first()

    async def create(  # type: ignore
        self, db: AsyncSession, *, obj_in: CategoryCreate, user_id: int, budget_id: int
    ) -> Category:
        db_obj = Category(
            name=obj_in.name,
            desc=obj_in.desc,
            amount=obj_in.amount,
            created_at=datetime.now(),
            user_id=user_id,
            budget_id=budget_id,
        )
        return await super().create(db, obj_in=db_obj)


category = CRUDCategory(Category)
