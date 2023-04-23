from asyncio import run
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from src.core.security import get_password_hash
from src.db.db import get_session
from src.models.account import Account
from src.models.budget import Budget
from src.models.category import Category
from src.models.filter import Filter
from src.models.transaction import Transaction
from src.models.user import User


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
        Account(name="Wells Fargo", account_type="checking", created_at=now, user_id=user.id),
        Account(name="BOA", account_type="savings", created_at=now, user_id=user.id),
    ]

    session.add_all(accounts)

    await session.commit()

    budgets = [
        Budget(name="my budget", amount=4000, created_at=now, user_id=user.id),
    ]

    session.add_all(budgets)

    await session.commit()

    categories = [
        Category(
            name="Unsorted",
            desc="All unsorted transactions",
            created_at=now,
            user_id=user.id,
            budget_id=budgets[0].id,
            amount=-1,
        ),
        Category(
            name="food", desc="things to eat", created_at=now, user_id=user.id, budget_id=budgets[0].id, amount=1000
        ),
        Category(
            name="shopping", desc="things to buy", created_at=now, user_id=user.id, budget_id=budgets[0].id, amount=1000
        ),
        Category(
            name="entertainment",
            desc="things to do",
            created_at=now,
            user_id=user.id,
            budget_id=budgets[0].id,
            amount=2000,
        ),
    ]

    session.add_all(categories)

    await session.commit()

    filters = [
        Filter(filter_by="panda express", created_at=now, user_id=user.id, category_id=categories[1].id),
        Filter(filter_by="macys", created_at=now, user_id=user.id, category_id=categories[2].id),
        Filter(filter_by="regal", created_at=now, user_id=user.id, category_id=categories[3].id),
    ]

    session.add_all(filters)

    await session.commit()

    transactions = [
        Transaction(
            amount=14.56,
            date=now,
            desc="panda express",
            created_at=now,
            user_id=user.id,
            category_id=categories[1].id,
            budget_id=budgets[0].id,
            account_id=accounts[0].id,
        ),
        Transaction(
            amount=100.21,
            date=now,
            desc="macys",
            created_at=now,
            user_id=user.id,
            category_id=categories[1].id,
            budget_id=budgets[0].id,
            account_id=accounts[0].id,
        ),
        Transaction(
            amount=14.56,
            date=now,
            desc="regal",
            created_at=now,
            user_id=user.id,
            category_id=categories[2].id,
            budget_id=budgets[0].id,
            account_id=accounts[1].id,
        ),
    ]

    session.add_all(transactions)

    await session.commit()


run(main())
