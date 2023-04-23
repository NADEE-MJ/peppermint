from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.models.filter import Filter, FilterCreate
from src.models.category import CategoryCreate


async def create_test_filter(db: AsyncSession, user_id: int, category_id: int) -> Filter:
    filter_create = FilterCreate(filter_by="test filter")
    filter = await crud.filter.create(db, obj_in=filter_create, user_id=user_id, category_id=category_id)

    return filter


async def create_parser_test_filters(db: AsyncSession, user_id: int, budget_id: int) -> Filter:
    categories_filters = [
        (
            CategoryCreate(desc="Stuff you need to stay alive.", name="Food and Drink", amount=1000),
            FilterCreate(filter_by="Panda Express"),
        ),
        (
            CategoryCreate(desc="Stuff you probably don't need.", name="Shopping", amount=1000),
            FilterCreate(filter_by="Macy's"),
        ),
        (
            CategoryCreate(desc="Stuff you are probably wasting your time on.", name="Entertainment", amount=1000),
            FilterCreate(filter_by="Regal Entertainment"),
        ),
    ]
    filters = []
    for category_create, filter_create in categories_filters:
        category = await crud.category.create(db, obj_in=category_create, user_id=user_id, budget_id=budget_id)
        filters.append(await crud.filter.create(db, obj_in=filter_create, user_id=user_id, category_id=category.id))

    return filters
