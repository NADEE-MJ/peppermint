from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.models.category import Category, CategoryCreate


async def create_test_category(db: AsyncSession, user_id: int, budget_id: int) -> Category:
    categories = await crud.category.get_all_categories_for_user(db, user_id=user_id)
    if categories:
        for category in categories:
            if category.name == "test category":
                return category

    category_create = CategoryCreate(desc="for testing", name="test category")
    category = await crud.category.create(db, obj_in=category_create, user_id=user_id, budget_id=budget_id)

    return category
