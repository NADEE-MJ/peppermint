from asyncio import run
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from src.core.security import get_password_hash
from src.db.db import get_session
from src.models.account import Account
from src.models.budget import Budget
from src.models.user import User
from src.models.filter import Filter
from src.models.category import Category
from src.models.transaction import Transaction


async def main() -> None:
    now = datetime.now()

    session: AsyncSession = [i async for i in get_session()][0]

    user = User(
        full_name="Admin Admin",
        email="admin@test.com",
        password=get_password_hash("Test1234!"),
        is_active=True,
        created_at=now,
        last_login=datetime.now(),
    )
    session.add(user)

    await session.commit()

    accounts = [
        Account(name="Wells Fargo", account_type="checking", created_at=now, user_id=1),
        Account(name="BOA", account_type="savings", created_at=now, user_id=1),
    ]

    session.add_all(accounts)

    await session.commit()

    budgets = [
        Budget(name="my budget", amount=4000, created_at=now, user_id=1),
        Budget(name="my second budget", amount=4000, created_at=now, user_id=1),
    ]

    session.add_all(budgets)

    await session.commit()

    categories = [
        Category(name="food", desc="things to eat", created_at=now, user_id=1, budget_id=1),
        Category(name="shopping", desc="things to buy", created_at=now, user_id=1, budget_id=1),
        Category(name="entertainmenet", desc="things to do", created_at=now, user_id=1, budget_id=2),
    ]

    session.add_all(categories)

    await session.commit()

    filters = [
        Filter(filter_by="panda express", created_at=now, user_id=1, category_id=1),
        Filter(filter_by="macys", created_at=now, user_id=1, category_id=2),
        Filter(filter_by="regal", created_at=now, user_id=1, category_id=3),
    ]

    session.add_all(filters)

    await session.commit()

    transactions = [
        Transaction(
            amount=14.56, date=now, desc="panda express", created_at=now, user_id=1, category_id=1, budget_id=1
        ),
        Transaction(amount=100.21, date=now, desc="macys", created_at=now, user_id=1, category_id=2, budget_id=1),
        Transaction(amount=14.56, date=now, desc="regal", created_at=now, user_id=1, category_id=3, budget_id=2),
    ]

    session.add_all(transactions)

    await session.commit()


run(main())
