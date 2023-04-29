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
    users = [
        User(
            full_name="Admin Admin",
            email="admin@test.com",
            password=get_password_hash("Test1234!"),
            is_active=True,
            created_at=now,
            is_admin=True,
            last_login=datetime.now(),
        ),
        User(
            full_name="Test User",
            email="user@test.com",
            password=get_password_hash("Test1234!"),
            is_active=True,
            created_at=now,
            is_admin=False,
            last_login=datetime.now(),
        ),
    ]

    session.add_all(users)

    await session.commit()

    accounts = [
        Account(name="Wells Fargo", account_type="checking", created_at=now, user_id=users[1].id),
        Account(name="BOA", account_type="savings", created_at=now, user_id=users[1].id),
    ]

    session.add_all(accounts)

    await session.commit()

    budgets = [
        Budget(name="my budget", amount=4000, created_at=now, user_id=users[1].id),
    ]

    session.add_all(budgets)

    await session.commit()

    categories = [
        Category(
            name="Unsorted",
            desc="All unsorted transactions.",
            created_at=now,
            user_id=users[1].id,
            budget_id=budgets[0].id,
            amount=-1,
        ),
        Category(
            name="Food and Drink",
            desc="Stuff you need to stay alive.",
            created_at=now,
            user_id=users[1].id,
            budget_id=budgets[0].id,
            amount=1000,
        ),
        Category(
            name="Shopping",
            desc="Stuff you probably don't need.",
            created_at=now,
            user_id=users[1].id,
            budget_id=budgets[0].id,
            amount=1000,
        ),
        Category(
            name="Entertainment",
            desc="Stuff you are probably wasting your time on.",
            created_at=now,
            user_id=users[1].id,
            budget_id=budgets[0].id,
            amount=2000,
        ),
    ]

    session.add_all(categories)

    await session.commit()

    filters = [
        Filter(filter_by="Panda Express", created_at=now, user_id=users[1].id, category_id=categories[1].id),
        Filter(filter_by="Macy's", created_at=now, user_id=users[1].id, category_id=categories[2].id),
        Filter(filter_by="Regal Entertainment", created_at=now, user_id=users[1].id, category_id=categories[3].id),
    ]

    session.add_all(filters)

    await session.commit()

    transactions = [
        Transaction(
            amount=14.56,
            date=now,
            desc="Panda Express - Brea #k1jh234",
            created_at=now,
            user_id=users[1].id,
            category_id=categories[1].id,
            budget_id=budgets[0].id,
            account_id=accounts[0].id,
        ),
        Transaction(
            amount=100.21,
            date=now,
            desc="Macy's Trans#lk2341g3",
            created_at=now,
            user_id=users[1].id,
            category_id=categories[1].id,
            budget_id=budgets[0].id,
            account_id=accounts[0].id,
        ),
        Transaction(
            amount=14.56,
            date=now,
            desc="Regal Entertainment LKJ3123",
            created_at=now,
            user_id=users[1].id,
            category_id=categories[2].id,
            budget_id=budgets[0].id,
            account_id=accounts[1].id,
        ),
    ]

    session.add_all(transactions)

    await session.commit()


run(main())
