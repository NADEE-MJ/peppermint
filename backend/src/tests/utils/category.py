from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.models.category import Category, CategoryCreate


async def create_test_category(db: AsyncSession, user_id: int, budget_id: int) -> Category:
    category_create = CategoryCreate(desc="for testing", name="test category", amount=100)
    category = await crud.category.create(db, obj_in=category_create, user_id=user_id, budget_id=budget_id)

    return category
