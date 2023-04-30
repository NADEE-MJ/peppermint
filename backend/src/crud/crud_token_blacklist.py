from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.crud.base import CRUDBase
from src.models.token_blacklist import (
    TokenBlacklist,
    TokenBlacklistCreate,
    TokenBlacklistUpdate,
)


class CRUDTokenBlackList(CRUDBase[TokenBlacklist, TokenBlacklistCreate, TokenBlacklistUpdate]):
    async def create(  # type: ignore
        self, db: AsyncSession, *, obj_in: TokenBlacklistCreate, user_id: int
    ) -> TokenBlacklist:
        db_obj = TokenBlacklist(token=obj_in.token, created_at=datetime.now(), user_id=user_id)
        return await super().create(db, obj_in=db_obj)

    async def get_by_token(self, db: AsyncSession, *, token: str) -> Optional[TokenBlacklist]:
        result = await db.execute(select(TokenBlacklist).filter(TokenBlacklist.token == token))
        return result.scalars().first()

    async def get_all_tokens_for_user(self, db: AsyncSession, *, user_id: int) -> Optional[list[TokenBlacklist]]:
        result = await db.execute(select(TokenBlacklist).filter(TokenBlacklist.user_id == user_id))
        return result.scalars().all()


token_blacklist = CRUDTokenBlackList(TokenBlacklist)
