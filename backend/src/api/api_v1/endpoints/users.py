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


@router.post("/", response_model=UserResponse)
async def create_user(
    *,
    db: AsyncSession = Depends(get_session),
    user_create: UserCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new user. Must Be logged in first.
    """
    user = await crud.user.get_by_email(db, email=user_create.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this username already exists in the system.",
        )
    user = await crud.user.user_create(db, obj_in=user_create)
    if settings.EMAILS_ENABLED:
        send_new_account_email(
            email=user_create.email,
            password=user_create.password,
        )
    return user


@router.put("/me", response_model=UserResponse)
async def update_user_me(
    *,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_user),
    user_update: UserUpdate,
) -> Any:
    """
    Update own user.
    """
    user = await crud.user.user_update(db, db_obj=current_user, obj_in=user_update)
    return user


@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/open", response_model=UserResponse)
async def create_user_open(*, db: AsyncSession = Depends(get_session), user_create: UserCreate) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = await crud.user.get_by_email(db, email=user_create.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user = await crud.user.user_create(db, obj_in=user_create)
    if settings.EMAILS_ENABLED:
        send_new_account_email(
            email=user_create.email,
            password=user_create.password,
        )
    return user
