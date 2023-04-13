import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.models.budget import BudgetCreate, BudgetUpdate
from src.tests.utils.budget import create_test_budget
from src.tests.utils.user import create_random_user


@pytest.mark.asyncio
async def test_create_budget(db: AsyncSession) -> None:
    user = await create_random_user(db)
    # code from create_test_budget copied for clarity
    budget = BudgetCreate(amount=400, name="test budget")
    budget_from_db = await crud.budget.create(db, obj_in=budget, user_id=user.id)

    # ? deletes user and associated budgets
    await crud.user.remove(db, id=user.id)
    assert budget_from_db
    assert budget_from_db.user_id == user.id


@pytest.mark.asyncio
async def test_get_all_budgets_for_user(db: AsyncSession) -> None:
    user = await create_random_user(db)
    await create_test_budget(db, user_id=user.id)
    budgets = await crud.budget.get_all_budgets_for_user(db, user_id=user.id)

    await crud.user.remove(db, id=user.id)
    assert len(budgets) == 1
    assert budgets[0].user_id == user.id


@pytest.mark.asyncio
async def test_update_budget(db: AsyncSession) -> None:
    user = await create_random_user(db)
    budget_from_db = await create_test_budget(db, user_id=user.id)
    budget = BudgetUpdate(name="updated test budget")
    budget_from_db = await crud.budget.update(db, db_obj=budget_from_db, obj_in=budget)

    await crud.user.remove(db, id=user.id)
    assert budget_from_db.name == budget.name
