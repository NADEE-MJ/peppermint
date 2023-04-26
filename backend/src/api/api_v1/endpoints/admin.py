from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.api import deps
from src.core.config import settings
from src.db.db import get_session
from src.models.user import User, UserCreate, UserResponse, UserUpdate
from src.utils import send_new_account_email

router = APIRouter()


@router.delete("/{user_id}", response_model=UserResponse)
async def remove_user(
    user_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Remove an existing user. Must be logged in first. Must be an admin.
    """
    user = await crud.user.get(db, id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="That user does not exist.")

    if user.is_admin:
        raise HTTPException(status_code=403, detail="Admin cannot be removed")
    user = await crud.user.remove(db, id=user_id)

    return user


@router.post("/", response_model=UserResponse)
async def create_user(
    user_create: UserCreate,
    is_admin: bool,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Create new user. Must be admin and logged in.
    """

    user = await crud.user.get_by_email(db, email=user_create.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user = await crud.user.create(db, admin=is_admin, obj_in=user_create)
    if settings.EMAILS_ENABLED:
        send_new_account_email(
            email=user_create.email,
            password=user_create.password,
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    *,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Update selected user.
    """
    user = await crud.user.update(db, db_obj=current_user, obj_in=user_update)
    return user
