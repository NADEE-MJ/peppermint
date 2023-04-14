from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.crud.base import CRUDBase
from src.models.transaction import Transaction, TransactionCreate, TransactionUpdate


class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    async def get_all_transactions_for_user(self, db: AsyncSession, *, user_id: int) -> Optional[list[Transaction]]:
        result = await db.execute(select(Transaction).filter(Transaction.user_id == user_id))
        return result.scalars().all()

    async def get_all_transactions_for_budget(
        self, db: AsyncSession, *, user_id: int, budget_id: int
    ) -> Optional[list[Transaction]]:
        result = await db.execute(
            select(Transaction).filter(Transaction.user_id == user_id).filter(Transaction.budget_id == budget_id)
        )
        return result.scalars().all()

    async def get_all_transactions_for_category_in_budget(
        self, db: AsyncSession, *, user_id: int, category_id: int, budget_id: int
    ) -> Optional[list[Transaction]]:
        result = await db.execute(
            select(Transaction)
            .filter(Transaction.user_id == user_id)
            .filter(Transaction.budget_id == budget_id)
            .filter(Transaction.category_id == category_id)
        )
        return result.scalars().all()

    async def get_all_transactions_for_category_in_account(
        self, db: AsyncSession, *, user_id: int, category_id: int, account_id: int
    ) -> Optional[list[Transaction]]:
        result = await db.execute(
            select(Transaction)
            .filter(Transaction.user_id == user_id)
            .filter(Transaction.account_id == account_id)
            .filter(Transaction.category_id == category_id)
        )
        return result.scalars().all()

    async def get_all_transactions_for_account(
        self, db: AsyncSession, *, user_id: int, account_id: int
    ) -> Optional[list[Transaction]]:
        result = await db.execute(
            select(Transaction).filter(Transaction.user_id == user_id).filter(Transaction.account_id == account_id)
        )
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: TransactionCreate, user_id: int, category_id: int, budget_id: int, account_id: int) -> Transaction:  # type: ignore
        db_obj = Transaction(
            amount=obj_in.amount,
            desc=obj_in.desc,
            date=datetime.fromisoformat(obj_in.date),
            created_at=datetime.now(),
            user_id=user_id,
            category_id=category_id,
            budget_id=budget_id,
            account_id=account_id,
        )
        return await super().create(db, obj_in=db_obj)  # type: ignore

    async def update(
        self, db: AsyncSession, *, db_obj: Transaction, obj_in: TransactionUpdate | Dict[str, Any]
    ) -> Transaction:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "date" in update_data and update_data["date"] is not None:
            update_data["date"] = datetime.fromisoformat(update_data["date"])
        elif "date" in update_data:
            del update_data["date"]
        return await super().update(db, db_obj=db_obj, obj_in=update_data)


transaction = CRUDTransaction(Transaction)
