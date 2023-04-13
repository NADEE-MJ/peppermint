from datetime import datetime
from typing import Any, Dict, Optional

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
        return await super().create(db, obj_in=db_obj)  # type: ignore

    async def update(self, db: AsyncSession, *, db_obj: Budget, obj_in: BudgetUpdate | Dict[str, Any]) -> Budget:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return await super().update(db, db_obj=db_obj, obj_in=update_data)


budget = CRUDBudget(Budget)
