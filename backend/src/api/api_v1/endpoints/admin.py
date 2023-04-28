from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.api import deps
from src.core.config import settings
from src.db.db import get_session
from src.models.user import User, UserCreate, UserResponse, UserUpdate
from src.utils import send_new_account_email

router = APIRouter()


@router.post("", response_model=UserResponse)
async def create_user(
    is_admin: bool,
    user_create: UserCreate,
    db: AsyncSession = Depends(get_session),
    current_admin: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Create new user or admin. Must be admin and logged in.
    """
    user = await crud.user.get_by_email(db, email=user_create.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists in the system",
        )
    user = await crud.user.create(db, is_admin=is_admin, obj_in=user_create)
    if settings.EMAILS_ENABLED:
        send_new_account_email(
            email=user_create.email,
            password=user_create.password,
        )
    return user


@router.delete("/user/{user_id}", response_model=UserResponse)
async def remove_user(
    user_id: int,
    db: AsyncSession = Depends(get_session),
    current_admin: User = Depends(deps.get_current_active_admin),
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


@router.put("/user/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_session),
    current_admin: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Update selected user, must be admin
    """
    user_to_update = await crud.user.get(db, id=user_id)

    if user_to_update is None:
        raise HTTPException(status_code=404, detail="That user does not exist.")

    if user_to_update.is_admin:
        raise HTTPException(status_code=403, detail="Admin cannot be updated by another admin")

    user = await crud.user.update(db, db_obj=user_to_update, obj_in=user_update)
    return user


@router.get("/user/{email}", response_model=UserResponse)
async def get_user_by_email(
    *,
    email: EmailStr,
    db: AsyncSession = Depends(get_session),
    current_admin: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Get user info by email, must be admin
    """
    user = await crud.user.get_by_email(db, email=email)
    if user is None:
        raise HTTPException(status_code=404, detail="That user does not exist.")
    return user


@router.get("", response_model=UserResponse)
async def read_user_me(
    current_admin: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Get current admin
    """
    return current_admin


@router.put("", response_model=UserResponse)
async def update_user_me(
    admin_update: UserUpdate,
    db: AsyncSession = Depends(get_session),
    current_admin: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Update Current Admin
    """
    admin = await crud.user.update(db, db_obj=current_admin, obj_in=admin_update)
    return admin
