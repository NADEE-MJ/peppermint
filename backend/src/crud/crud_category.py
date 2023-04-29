from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.crud.base import CRUDBase
from src.models.category import Category, CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    async def get_all_categories_for_user(self, db: AsyncSession, *, user_id: int) -> Optional[list[Category]]:
        result = await db.execute(select(Category).filter(Category.user_id == user_id))
        return result.scalars().all()

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
