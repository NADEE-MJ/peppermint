from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.crud.base import CRUDBase
from src.models.budget import Budget, BudgetCreate, BudgetUpdate


class CRUDBudget(CRUDBase[Budget, BudgetCreate, BudgetUpdate]):
    async def get_all_budgets_for_user(self, db: AsyncSession, *, user_id: int) -> Optional[list[Budget]]:
        result = await db.execute(select(Budget).filter(Budget.user_id == user_id))
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: BudgetCreate, user_id: int) -> Budget:  # type: ignore
        db_obj = Budget(name=obj_in.name, amount=obj_in.amount, created_at=datetime.now(), user_id=user_id)
        return await super().create(db, obj_in=db_obj)


budget = CRUDBudget(Budget)
