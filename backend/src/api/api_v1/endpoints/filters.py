from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.api import deps
from src.db.db import get_session
from src.models.filter import FilterCreate, FilterResponse, FilterUpdate
from src.models.user import User

router = APIRouter()


@router.get("", response_model=list[FilterResponse])
async def get_all_filters(
    page: int = 0,
    limit: int = 10,
    *,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all filters for current user.
    """
    if current_user.id is not None:
        filters = await crud.filter.get_all_filters_for_user(db, user_id=current_user.id, page=page, limit=limit)

        return filters


@router.get("/category/{category_id}", response_model=list[FilterResponse])
async def get_all_filters_by_category(
    category_id: int,
    page: int = 0,
    limit: int = 10,
    *,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all filters for current user by category.
    """
    if current_user.id is not None:
        # check if category belongs to that user
        category = await crud.category.get(db, id=category_id)

        if category is None:
            raise HTTPException(status_code=404, detail="That category does not exist.")

        if category.user_id != current_user.id:
            raise HTTPException(status_code=401, detail="You are unauthorized to add a filter to this category")

        filters = await crud.filter.get_all_filters_for_category(
            db, user_id=current_user.id, category_id=category_id, page=page, limit=limit
        )

        return filters


@router.get("/{filter_id}", response_model=FilterResponse)
async def get_filter(
    filter_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get specific filter info for current user.
    """
    filter = await crud.filter.get(db, id=filter_id)
    if filter is None:
        raise HTTPException(status_code=404, detail="That filter does not exist.")

    if filter.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="You are unauthorized to access this filter")
    return filter


@router.post("/category/{category_id}", response_model=FilterResponse)
async def create_filter(
    category_id: int,
    *,
    db: AsyncSession = Depends(get_session),
    filter_create: FilterCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new filter. Must Be logged in first.
    """
    if current_user.id is not None:
        # check if category belongs to that user
        category = await crud.category.get(db, id=category_id)

        if category is None:
            raise HTTPException(status_code=404, detail="That category does not exist.")

        if category.user_id != current_user.id:
            raise HTTPException(status_code=401, detail="You are unauthorized to add a filter to this category")

        # check if filter filter_by already exists
        filters = await crud.filter.get_all_filters_for_user(db, user_id=current_user.id)

        if filters is not None:
            for filter in filters:
                if filter.filter_by == filter_create.filter_by:
                    raise HTTPException(
                        status_code=400,
                        detail="A filter with that filter_by already exists in the system.",
                    )

        filter = await crud.filter.create(db, obj_in=filter_create, user_id=current_user.id, category_id=category_id)

        return filter


@router.put("/{filter_id}", response_model=FilterResponse)
async def update_filter(
    filter_id: int,
    filter_update: FilterUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an existing filter. Must be logged in first.
    """
    filter_from_db = await crud.filter.get(db, id=filter_id)

    if filter_from_db is None:
        raise HTTPException(status_code=404, detail="That filter does not exist.")

    if filter_from_db.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="You are unauthorized to update this filter")

    filters = await crud.filter.get_all_filters_for_user(db, user_id=current_user.id)

    if filters is not None:
        for filter in filters:
            if filter.filter_by == filter_update.filter_by:
                raise HTTPException(
                    status_code=400,
                    detail="A filter with that filter_by already exists in the system.",
                )

    filter = await crud.filter.update(db, db_obj=filter_from_db, obj_in=filter_update)

    return filter


@router.delete("/{filter_id}", response_model=FilterResponse)
async def remove_filter(
    filter_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove an existing filter. Must be logged in first.
    """
    filter = await crud.filter.get(db, id=filter_id)

    if filter is None:
        raise HTTPException(status_code=404, detail="That filter does not exist.")

    if filter.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="You are unauthorized to remove this filter")

    filter = await crud.filter.remove(db, id=filter_id)

    return filter
