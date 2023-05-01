from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.api import deps
from src.db.db import get_session
from src.models.category import CategoryCreate, CategoryResponse, CategoryUpdate
from src.models.user import User

router = APIRouter()


@router.get("", response_model=dict[str, int | list[CategoryResponse]])
async def get_all_categories(
    page: int = 0,
    limit: int = 10,
    *,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all categories for current user.
    """
    if current_user.id is not None:
        categories = await crud.category.get_all_categories_for_user(
            db, user_id=current_user.id, page=page, limit=limit
        )

        return categories


@router.get("/budget/{budget_id}", response_model=list[CategoryResponse])
async def get_all_categories_by_budget(
    budget_id: int,
    *,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all categories for current user by budget.
    """
    if current_user.id is not None:
        # check if budget belongs to that user
        budget = await crud.budget.get(db, id=budget_id)

        if budget is None:
            raise HTTPException(status_code=404, detail="That budget does not exist.")

        if budget.user_id != current_user.id:
            raise HTTPException(status_code=401, detail="You are unauthorized to add a category to this budget")

        categories = await crud.category.get_all_categories_for_budget(db, user_id=current_user.id, budget_id=budget_id)

        return categories


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get specific category info for current user.
    """
    category = await crud.category.get(db, id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="That category does not exist.")

    if category.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="You are unauthorized to access this category")
    return category


@router.post("/budget/{budget_id}", response_model=CategoryResponse)
async def create_category(
    budget_id: int,
    *,
    db: AsyncSession = Depends(get_session),
    category_create: CategoryCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new category. Must Be logged in first.
    """
    if current_user.id is not None:
        # check if budget belongs to that user
        budget = await crud.budget.get(db, id=budget_id)

        if budget is None:
            raise HTTPException(status_code=404, detail="That budget does not exist.")

        if budget.user_id != current_user.id:
            raise HTTPException(status_code=401, detail="You are unauthorized to add a category to this budget")

        # check if category name already exists
        data = await crud.category.get_all_categories_for_user(db, user_id=current_user.id, limit=-1)

        if data is not None:
            categories = data["paginated_results"]
            if categories is not None and isinstance(categories, list):
                for category in categories:
                    if category.name == category_create.name:
                        raise HTTPException(
                            status_code=400,
                            detail="A category with the name already exists in the system.",
                        )

        category = await crud.category.create(db, obj_in=category_create, user_id=current_user.id, budget_id=budget_id)

        return category


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an existing category. Must be logged in first.
    """
    category_from_db = await crud.category.get(db, id=category_id)

    if category_from_db is None:
        raise HTTPException(status_code=404, detail="That category does not exist.")

    if category_from_db.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="You are unauthorized to update this category")

    data = await crud.category.get_all_categories_for_user(db, user_id=current_user.id, limit=-1)

    if data is not None:
        categories = data["paginated_results"]

    if categories is not None and category_update.name is not None and category_update.name != category_from_db.name:
        if isinstance(categories, list):
            for category in categories:
                if category.name == category_update.name:
                    raise HTTPException(
                        status_code=400,
                        detail="A category with the name already exists in the system.",
                    )

    category = await crud.category.update(db, db_obj=category_from_db, obj_in=category_update)

    return category


@router.delete("/{category_id}", response_model=CategoryResponse)
async def remove_category(
    category_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove an existing category. Must be logged in first.
    """
    category = await crud.category.get(db, id=category_id)

    if category is None:
        raise HTTPException(status_code=404, detail="That category does not exist.")

    if category.name == "Unsorted":
        raise HTTPException(status_code=400, detail="You cannot remove the Unsorted category.")

    if category.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="You are unauthorized to remove this category")

    category = await crud.category.remove(db, id=category_id)

    return category
