import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.models.category import CategoryCreate, CategoryUpdate
from src.tests.utils.category import create_test_category
from src.tests.utils.budget import create_test_budget
from src.tests.utils.user import create_random_user


@pytest.mark.asyncio
async def test_create_category(db: AsyncSession) -> None:
    user = await create_random_user(db)
    budget = await create_test_budget(db, user_id=user.id)
    # code from create_test_category copied for clarity
    category = CategoryCreate(desc="for testing", name="test category")
    category_from_db = await crud.category.create(db, obj_in=category, user_id=user.id, budget_id=budget.id)

    # ? deletes user and associated categories
    await crud.user.remove(db, id=user.id)
    assert category_from_db
    assert category_from_db.user_id == user.id


@pytest.mark.asyncio
async def test_get_all_categories_for_user(db: AsyncSession) -> None:
    user = await create_random_user(db)
    budget = await create_test_budget(db, user_id=user.id)
    await create_test_category(db, user_id=user.id, budget_id=budget.id)
    categories = await crud.category.get_all_categories_for_user(db, user_id=user.id)

    await crud.user.remove(db, id=user.id)
    assert len(categories) == 1
    assert categories[0].user_id == user.id


@pytest.mark.asyncio
async def test_get_all_categories_for_budget(db: AsyncSession) -> None:
    user = await create_random_user(db)
    budget = await create_test_budget(db, user_id=user.id)
    await create_test_category(db, user_id=user.id, budget_id=budget.id)
    categories = await crud.category.get_all_categories_for_budget(db, user_id=user.id, budget_id=budget.id)

    await crud.user.remove(db, id=user.id)
    assert len(categories) == 1
    assert categories[0].user_id == user.id
