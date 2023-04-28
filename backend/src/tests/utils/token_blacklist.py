from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from src.models.token_blacklist import TokenBlacklist
from src.tests.utils.utils import random_token


async def create_test_token_blacklist(
    db: AsyncSession, user_id: int, *, date: datetime | None = None, token: str | None = None
) -> TokenBlacklist:
    if token is None:
        token = random_token()
    if date is None:
        date = datetime.now()
    token_blacklist = TokenBlacklist(
        token=token,
        created_at=date,
        user_id=user_id,
    )
    db.add(token_blacklist)
    await db.commit()
    await db.refresh(token_blacklist)

    return token_blacklist
