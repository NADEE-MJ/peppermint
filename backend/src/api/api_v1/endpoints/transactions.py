from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.api import deps
from src.core.parser import parser
from src.db.db import get_session
from src.models.json_msg import JsonMsgSuccess
from src.models.transaction import (
    ParseCSV,
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
)
from src.models.user import User

router = APIRouter()


@router.get("", response_model=dict[str, int | list[TransactionResponse]])
async def get_all_transactions(
    page: int = 0,
    limit: int = 10,
    *,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all transactions for current user.
    """
    if current_user.id is not None:
        data = await crud.transaction.get_all_transactions_for_user(db, user_id=current_user.id, page=page, limit=limit)

        return data


@router.get("/budget/{budget_id}", response_model=dict[str, int | list[TransactionResponse]])
async def get_all_transactions_by_budget(
    budget_id: int,
    page: int = 0,
    limit: int = 10,
    *,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all transactions for current user by budget.
    """
    if current_user.id is not None:
        # check if budget belongs to that user
        budget = await crud.budget.get(db, id=budget_id)

        if budget is None:
            raise HTTPException(status_code=404, detail="That budget does not exist.")

        if budget.user_id != current_user.id:
            raise HTTPException(status_code=401, detail="You are unauthorized to add a transaction to this budget")

        data = await crud.transaction.get_all_transactions_for_budget(
            db, user_id=current_user.id, budget_id=budget_id, page=page, limit=limit
        )

        return data


@router.get("/budget/{budget_id}/from/{from_date}/to/{to_date}", response_model=list[TransactionResponse])
async def get_all_transactions_by_budget_and_date_range(
    budget_id: int,
    from_date: datetime,
    to_date: datetime,
    *,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all transactions for current user by budget.
    """
    from_date = datetime.strptime(from_date.isoformat().split("T")[0], "%Y-%m-%d")
    to_date = datetime.strptime(to_date.isoformat().split("T")[0], "%Y-%m-%d")
    if current_user.id is not None:
        # check if budget belongs to that user
        budget = await crud.budget.get(db, id=budget_id)

        if budget is None:
            raise HTTPException(status_code=404, detail="That budget does not exist.")

        if budget.user_id != current_user.id:
            raise HTTPException(status_code=401, detail="You are unauthorized to add a transaction to this budget")

        data = await crud.transaction.get_all_transactions_for_budget_and_date_range(
            db, user_id=current_user.id, budget_id=budget_id, from_date=from_date, to_date=to_date
        )

        return data if data else []


@router.get("/account/{account_id}", response_model=dict[str, int | list[TransactionResponse]])
async def get_all_transactions_by_account(
    account_id: int,
    page: int = 0,
    limit: int = 10,
    *,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all transactions for current user by account.
    """
    if current_user.id is not None:
        # check if account belongs to that user
        account = await crud.account.get(db, id=account_id)

        if account is None:
            raise HTTPException(status_code=404, detail="That account does not exist.")

        if account.user_id != current_user.id:
            raise HTTPException(status_code=401, detail="You are unauthorized to add a transaction to this account")

        data = await crud.transaction.get_all_transactions_for_account(
            db, user_id=current_user.id, account_id=account_id, page=page, limit=limit
        )

        return data


@router.get("/budget/{budget_id}/category/{category_id}", response_model=dict[str, int | list[TransactionResponse]])
async def get_all_transactions_by_budget_and_category(
    budget_id: int,
    category_id: int,
    page: int = 0,
    limit: int = 10,
    *,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all transactions for current user by budget and category.
    """
    if current_user.id is not None:
        # check if budget belongs to that user
        budget = await crud.budget.get(db, id=budget_id)

        if budget is None:
            raise HTTPException(status_code=404, detail="That budget does not exist.")

        if budget.user_id != current_user.id:
            raise HTTPException(status_code=401, detail="You are unauthorized to add a transaction to this budget")

        # check if category belongs to that user
        category = await crud.category.get(db, id=category_id)

        if category is None:
            raise HTTPException(status_code=404, detail="That category does not exist.")

        if category.user_id != current_user.id:
            raise HTTPException(status_code=401, detail="You are unauthorized to add a transaction to this category")

        data = await crud.transaction.get_all_transactions_for_category_in_budget(
            db, user_id=current_user.id, category_id=category_id, budget_id=budget_id, page=page, limit=limit
        )

        return data


@router.get("/account/{account_id}/category/{category_id}", response_model=dict[str, int | list[TransactionResponse]])
async def get_all_transactions_by_account_and_category(
    account_id: int,
    category_id: int,
    page: int = 0,
    limit: int = 10,
    *,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all transactions for current user by account and category.
    """
    if current_user.id is not None:
        # check if account belongs to that user
        account = await crud.account.get(db, id=account_id)

        if account is None:
            raise HTTPException(status_code=404, detail="That account does not exist.")

        if account.user_id != current_user.id:
            raise HTTPException(status_code=401, detail="You are unauthorized to add a transaction to this account")

        # check if category belongs to that user
        category = await crud.category.get(db, id=category_id)

        if category is None:
            raise HTTPException(status_code=404, detail="That category does not exist.")

        if category.user_id != current_user.id:
            raise HTTPException(status_code=401, detail="You are unauthorized to add a transaction to this category")

        data = await crud.transaction.get_all_transactions_for_category_in_account(
            db, user_id=current_user.id, category_id=category_id, account_id=account_id, page=page, limit=limit
        )

        return data


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get specific transaction info for current user.
    """
    transaction = await crud.transaction.get(db, id=transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="That transaction does not exist.")

    if transaction.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="You are unauthorized to access this transaction")
    return transaction


@router.post("/budget/{budget_id}/category/{category_id}/account/{account_id}", response_model=TransactionResponse)
async def create_transaction(
    budget_id: int,
    category_id: int,
    account_id: int,
    *,
    db: AsyncSession = Depends(get_session),
    transaction_create: TransactionCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new transaction. Must Be logged in first.
    """
    if current_user.id is not None:
        # check if budget belongs to that user
        budget = await crud.budget.get(db, id=budget_id)

        if budget is None:
            raise HTTPException(status_code=404, detail="That budget does not exist.")

        if budget.user_id != current_user.id:
            raise HTTPException(status_code=401, detail="You are unauthorized to add a transaction to this budget")

        # check if category belongs to that user
        category = await crud.category.get(db, id=category_id)

        if category is None:
            raise HTTPException(status_code=404, detail="That category does not exist.")

        if category.user_id != current_user.id:
            raise HTTPException(status_code=401, detail="You are unauthorized to add a transaction to this category")

        # check if category belongs to that user
        account = await crud.account.get(db, id=account_id)

        if account is None:
            raise HTTPException(status_code=404, detail="That account does not exist.")

        if account.user_id != current_user.id:
            raise HTTPException(status_code=401, detail="You are unauthorized to add a transaction to this account")

        # ! need to add some sort of duplicate transaction check here
        # ! a couple ways to do this could be to ask the user if they are sure they
        # ! want to add a duplicate transaction

        transaction = await crud.transaction.create(
            db,
            obj_in=transaction_create,
            user_id=current_user.id,
            category_id=category_id,
            budget_id=budget_id,
            account_id=account_id,
        )

        return transaction


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an existing transaction. Must be logged in first.
    """
    transaction_from_db = await crud.transaction.get(db, id=transaction_id)

    if transaction_from_db is None:
        raise HTTPException(status_code=404, detail="That transaction does not exist.")

    if transaction_from_db.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="You are unauthorized to update this transaction")

    # ! need to add some sort of duplicate transaction check here
    # ! a couple ways to do this could be to ask the user if they are sure they
    # ! want to add a duplicate transaction

    transaction = await crud.transaction.update(db, db_obj=transaction_from_db, obj_in=transaction_update)

    return transaction


@router.delete("/{transaction_id}", response_model=TransactionResponse)
async def remove_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove an existing transaction. Must be logged in first.
    """
    transaction = await crud.transaction.get(db, id=transaction_id)

    if transaction is None:
        raise HTTPException(status_code=404, detail="That transaction does not exist.")

    if transaction.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="You are unauthorized to remove this transaction")

    transaction = await crud.transaction.remove(db, id=transaction_id)

    return transaction


@router.post("/parse/budget/{budget_id}/account/{account_id}", response_model=JsonMsgSuccess)
async def parse_transactions_from_csv(
    budget_id: int,
    account_id: int,
    input: ParseCSV,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Parse a csv file. Must be logged in first.
    """
    mapping = input.mapping

    if current_user.id is not None:
        # check if budget belongs to that user
        budget = await crud.budget.get(db, id=budget_id)

        if budget is None:
            raise HTTPException(status_code=404, detail="That budget does not exist.")

        if budget.user_id != current_user.id:
            raise HTTPException(status_code=401, detail="You are unauthorized to add transactions to this budget")

        # check if account belongs to that user
        account = await crud.account.get(db, id=account_id)

        if account is None:
            raise HTTPException(status_code=404, detail="That account does not exist.")

        if account.user_id != current_user.id:
            raise HTTPException(status_code=401, detail="You are unauthorized to add a transaction to this account")

        csv_file = input.file
        if "csv" not in csv_file.split(",")[0]:
            raise HTTPException(status_code=422, detail="File is not a csv file.")

        return_value = await parser(
            db,
            mapping=mapping,
            file=csv_file,
            user_id=current_user.id,
            budget_id=budget_id,
            account_id=account_id,
        )

    return {"message": "Finished Parsing", "success": return_value}
