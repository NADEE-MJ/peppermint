from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.models.filter import Filter, FilterCreate


async def create_test_filter(db: AsyncSession, user_id: int, category_id: int) -> Filter:
    filters = await crud.filter.get_all_filters_for_user(db, user_id=user_id)
    if filters:
        for filter in filters:
            if filter.filter_by == "test filter":
                return filter

    filter_create = FilterCreate(filter_by="test filter")
    filter = await crud.filter.create(db, obj_in=filter_create, user_id=user_id, category_id=category_id)

    return filter
