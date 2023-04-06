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
    account_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: Account = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get specific bank account info for current user.
    """
    account = await crud.account.get(db, id=account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="That account does not exist.")

    if account.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="You are unauthorized to access this bank account")

    return account


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

    account = await crud.account.create(db, obj_in=account_create, user_id=current_user.id)

    return account


@router.put("/{account_id}", response_model=AccountResponse)
async def update_account(
    account_id: int,
    account_update: AccountUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: Account = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an existing bank account. Must be logged in first.
    """
    account = await crud.account.get(db, id=account_id)

    if account is None:
        raise HTTPException(status_code=404, detail="That account does not exist.")

    if account.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="You are unauthorized to update this bank account")

    accounts = await crud.account.get_all_accounts_for_user(db, user_id=current_user.id)

    for account in accounts:
        if account.name == account_update.name:
            raise HTTPException(
                status_code=400,
                detail="An account with the name already exists in the system.",
            )

    account = await crud.account.update(db, db_obj=account, obj_in=account_update)

    return account


@router.delete("/{account_id}", response_model=AccountResponse)
async def remove_account(
    account_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: Account = Depends(deps.get_current_active_user),
):
    """
    Remove an existing bank account. Must be logged in first.
    """
    account = await crud.account.get(db, id=account_id)

    if account is None:
        raise HTTPException(status_code=404, detail="That account does not exist.")

    if account.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="You are unauthorized to remove this bank account")

    account = await crud.account.remove(db, id=account_id)

    return account
