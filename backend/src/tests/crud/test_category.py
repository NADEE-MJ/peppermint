import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.models.category import CategoryCreate
from src.tests.utils.budget import create_test_budget
from src.tests.utils.category import create_test_category
from src.tests.utils.user import create_random_user


@pytest.mark.asyncio
async def test_create_category(db: AsyncSession) -> None:
    user = await create_random_user(db)
    budget = await create_test_budget(db, user_id=user.id)
    # code from create_test_category copied for clarity
    category = CategoryCreate(desc="for testing", name="test category", amount=1000)
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
    data = await crud.category.get_all_categories_for_user(db, user_id=user.id)

    categories = data["paginated_results"]
    total_pages = data["total_pages"]

    await crud.user.remove(db, id=user.id)
    assert total_pages == 1
    assert len(categories) == 2
    assert categories[0].user_id == user.id


@pytest.mark.asyncio
async def test_get_unsorted_category_for_budget(db: AsyncSession) -> None:
    user = await create_random_user(db)
    budget = await create_test_budget(db, user_id=user.id)
    category = await crud.category.get_unsorted_category_for_budget(db, user_id=user.id, budget_id=budget.id)

    await crud.user.remove(db, id=user.id)
    assert category.name == "Unsorted"


@pytest.mark.asyncio
async def test_get_all_categories_for_budget(db: AsyncSession) -> None:
    user = await create_random_user(db)
    budget = await create_test_budget(db, user_id=user.id)
    await create_test_category(db, user_id=user.id, budget_id=budget.id)
    categories = await crud.category.get_all_categories_for_budget(db, user_id=user.id, budget_id=budget.id)

    await crud.user.remove(db, id=user.id)
    assert len(categories) == 2
    assert categories[0].user_id == user.id
