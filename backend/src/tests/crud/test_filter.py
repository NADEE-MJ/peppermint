import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.models.filter import FilterCreate, FilterUpdate
from src.tests.utils.filter import create_test_filter
from src.tests.utils.category import create_test_category
from src.tests.utils.budget import create_test_budget
from src.tests.utils.user import create_random_user


@pytest.mark.asyncio
async def test_create_filter(db: AsyncSession) -> None:
    user = await create_random_user(db)
    budget = await create_test_budget(db, user_id=user.id)
    category = await create_test_category(db, user_id=user.id, budget_id=budget.id)
    # code from create_test_filter copied for clarity
    filter = FilterCreate(filter_by="test filter")
    filter_from_db = await crud.filter.create(db, obj_in=filter, user_id=user.id, category_id=category.id)

    # ? deletes user and associated filters
    await crud.user.remove(db, id=user.id)
    assert filter_from_db
    assert filter_from_db.user_id == user.id


@pytest.mark.asyncio
async def test_get_all_filters_for_user(db: AsyncSession) -> None:
    user = await create_random_user(db)
    budget = await create_test_budget(db, user_id=user.id)
    category = await create_test_category(db, user_id=user.id, budget_id=budget.id)
    await create_test_filter(db, user_id=user.id, category_id=category.id)
    filters = await crud.filter.get_all_filters_for_user(db, user_id=user.id)

    await crud.user.remove(db, id=user.id)
    assert len(filters) == 1
    assert filters[0].user_id == user.id


@pytest.mark.asyncio
async def test_get_all_filters_for_category(db: AsyncSession) -> None:
    user = await create_random_user(db)
    budget = await create_test_budget(db, user_id=user.id)
    category = await create_test_category(db, user_id=user.id, budget_id=budget.id)
    await create_test_filter(db, user_id=user.id, category_id=category.id)
    filters = await crud.filter.get_all_filters_for_category(db, user_id=user.id, category_id=category.id)

    await crud.user.remove(db, id=user.id)
    assert len(filters) == 1
    assert filters[0].user_id == user.id
