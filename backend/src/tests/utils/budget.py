from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.models.budget import Budget, BudgetCreate
from src.models.category import CategoryCreate


async def create_test_budget(db: AsyncSession, user_id: int) -> Budget:
    budget_create = BudgetCreate(amount=1000, name="test budget")
    budget = await crud.budget.create(db, obj_in=budget_create, user_id=user_id)

    category_create = CategoryCreate(desc="All unsorted transactions", name="Unsorted", amount=-1)
    await crud.category.create(db, obj_in=category_create, user_id=user_id, budget_id=budget.id)

    return budget
