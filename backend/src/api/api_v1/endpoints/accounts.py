from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.api import deps
from src.db.db import get_session
from src.models.account import Account, AccountCreate, AccountResponse, AccountUpdate

router = APIRouter()


@router.get("/", response_model=list[AccountResponse])
async def get_all_accounts(
    *,
    db: AsyncSession = Depends(get_session),
    current_user: Account = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all bank accounts for current user.
    """

    accounts = await crud.account.get_all_accounts_for_user(db, user_id=current_user.id)

    return accounts


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(
    *,
    account_id: AsyncSession = Depends(get_session),
    current_user: Account = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all bank accounts for current user.
    """

    accounts = await crud.account.get_all_accounts_for_user(db, user_id=current_user.id)

    return accounts


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
    accounts = await crud.account.get_all_accounts_for_user(db, user_id=current_user.id)

    for account in accounts:
        if account.name == account_create.name:
            raise HTTPException(
                status_code=400,
                detail="An account with the name already exists in the system.",
            )

    Account = await crud.Account.create(db, obj_in=account_create)

    return Account
