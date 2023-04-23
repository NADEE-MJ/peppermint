from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.models.transaction import Transaction, TransactionCreate


async def create_test_transaction(
    db: AsyncSession, user_id: int, category_id: int, budget_id: int, account_id: int
) -> Transaction:
    transaction_create = TransactionCreate(amount=400, date="05/01/2023", desc="test transaction")
    transaction = await crud.transaction.create(
        db,
        obj_in=transaction_create,
        user_id=user_id,
        account_id=account_id,
        budget_id=budget_id,
        category_id=category_id,
    )

    return transaction
