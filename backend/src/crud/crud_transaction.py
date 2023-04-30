from datetime import datetime
from math import ceil
from typing import Any, Dict, Optional

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.crud.base import CRUDBase
from src.models.transaction import Transaction, TransactionCreate, TransactionUpdate


class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    async def get_all_transactions_for_user(
        self, db: AsyncSession, *, user_id: int, page: int = 0, limit: int = 10
    ) -> Optional[dict[str, int | list[Transaction]]]:
        page *= limit
        paginated_results = (
            (await db.execute(select(Transaction).filter(Transaction.user_id == user_id).offset(page).limit(limit)))
            .scalars()
            .all()
        )

        count = (
            (await db.execute(select(func.count(Transaction.id)).filter(Transaction.user_id == user_id)))
            .scalars()
            .first()
        )
        if count is not None:
            total_pages = ceil(count / limit)
        else:
            total_pages = 0

        return {"paginated_results": paginated_results, "total_pages": total_pages}

    async def get_all_transactions_for_budget(
        self, db: AsyncSession, *, user_id: int, budget_id: int, page: int = 0, limit: int = 10
    ) -> Optional[dict[str, int | list[Transaction]]]:
        page *= limit
        paginated_results = (
            (
                await db.execute(
                    select(Transaction)
                    .filter(Transaction.user_id == user_id)
                    .filter(Transaction.budget_id == budget_id)
                    .offset(page)
                    .limit(limit)
                )
            )
            .scalars()
            .all()
        )

        count = (
            (
                await db.execute(
                    select(func.count(Transaction.id))
                    .filter(Transaction.user_id == user_id)
                    .filter(Transaction.budget_id == budget_id)
                )
            )
            .scalars()
            .first()
        )
        if count is not None:
            total_pages = ceil(count / limit)
        else:
            total_pages = 0

        return {"paginated_results": paginated_results, "total_pages": total_pages}

    async def get_all_transactions_for_category_in_budget(
        self, db: AsyncSession, *, user_id: int, category_id: int, budget_id: int, page: int = 0, limit: int = 10
    ) -> Optional[dict[str, int | list[Transaction]]]:
        page *= limit
        paginated_results = (
            (
                await db.execute(
                    select(Transaction)
                    .filter(Transaction.user_id == user_id)
                    .filter(Transaction.budget_id == budget_id)
                    .filter(Transaction.category_id == category_id)
                    .offset(page)
                    .limit(limit)
                )
            )
            .scalars()
            .all()
        )

        count = (
            (
                await db.execute(
                    select(func.count(Transaction.id))
                    .filter(Transaction.user_id == user_id)
                    .filter(Transaction.budget_id == budget_id)
                    .filter(Transaction.category_id == category_id)
                )
            )
            .scalars()
            .first()
        )
        if count is not None:
            total_pages = ceil(count / limit)
        else:
            total_pages = 0

        return {"paginated_results": paginated_results, "total_pages": total_pages}

    async def get_all_transactions_for_category_in_account(
        self, db: AsyncSession, *, user_id: int, category_id: int, account_id: int, page: int = 0, limit: int = 10
    ) -> Optional[dict[str, int | list[Transaction]]]:
        page *= limit
        paginated_results = (
            (
                await db.execute(
                    select(Transaction)
                    .filter(Transaction.user_id == user_id)
                    .filter(Transaction.account_id == account_id)
                    .filter(Transaction.category_id == category_id)
                    .offset(page)
                    .limit(limit)
                )
            )
            .scalars()
            .all()
        )

        count = (
            (
                await db.execute(
                    select(func.count(Transaction.id))
                    .filter(Transaction.user_id == user_id)
                    .filter(Transaction.account_id == account_id)
                    .filter(Transaction.category_id == category_id)
                )
            )
            .scalars()
            .first()
        )
        if count is not None:
            total_pages = ceil(count / limit)
        else:
            total_pages = 0

        return {"paginated_results": paginated_results, "total_pages": total_pages}

    async def get_all_transactions_for_account(
        self, db: AsyncSession, *, user_id: int, account_id: int, page: int = 0, limit: int = 10
    ) -> Optional[dict[str, int | list[Transaction]]]:
        page *= limit
        paginated_results = (
            (
                await db.execute(
                    select(Transaction)
                    .filter(Transaction.user_id == user_id)
                    .filter(Transaction.account_id == account_id)
                    .offset(page)
                    .limit(limit)
                )
            )
            .scalars()
            .all()
        )

        count = (
            (
                await db.execute(
                    select(func.count(Transaction.id))
                    .filter(Transaction.user_id == user_id)
                    .filter(Transaction.account_id == account_id)
                )
            )
            .scalars()
            .first()
        )
        if count is not None:
            total_pages = ceil(count / limit)
        else:
            total_pages = 0

        return {"paginated_results": paginated_results, "total_pages": total_pages}

    async def create(  # type: ignore
        self,
        db: AsyncSession,
        *,
        obj_in: TransactionCreate,
        user_id: int,
        category_id: int,
        budget_id: int,
        account_id: int,
    ) -> Transaction:
        db_obj = Transaction(
            amount=obj_in.amount,
            desc=obj_in.desc,
            date=(
                datetime.fromisoformat(obj_in.date).replace(tzinfo=None)
                if "T" in obj_in.date
                else datetime.strptime(obj_in.date, "%m/%d/%Y")
            ),
            created_at=datetime.now(),
            user_id=user_id,
            category_id=category_id,
            budget_id=budget_id,
            account_id=account_id,
        )
        return await super().create(db, obj_in=db_obj)

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
