from datetime import datetime
from typing import Any, Dict, Optional

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

    async def create(self, db: AsyncSession, *, obj_in: CategoryCreate, user_id: int, budget_id: int) -> Category:  # type: ignore
        db_obj = Category(
            name=obj_in.name, desc=obj_in.desc, created_at=datetime.now(), user_id=user_id, budget_id=budget_id
        )
        return await super().create(db, obj_in=db_obj)  # type: ignore


category = CRUDCategory(Category)