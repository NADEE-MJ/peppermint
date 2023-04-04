from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.api import deps
from src.core.config import settings
from src.db.db import get_session
from src.models.account import Account, AccountCreate, AccountResponse, AccountUpdate

router = APIRouter()


@router.post("/", response_model=AccountResponse)
async def create_account(
    *,
    db: AsyncSession = Depends(get_session),
    account_create: AccountCreate,
    current_user: Account = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new bank account. Must Be logged in first.
    """
    Account = await crud.account.get_all_accounts_for_user(db, user_id=current_user.id)
    if Account:
        raise HTTPException(
            status_code=400,
            detail="A Account with this Accountname already exists in the system.",
        )
    Account = await crud.Account.create(db, obj_in=Account_create)
    if settings.EMAILS_ENABLED:
        send_new_account_email(
            email=Account_create.email,
            password=Account_create.password,
        )
    return Account
