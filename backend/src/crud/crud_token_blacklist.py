from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.crud.base import CRUDBase
from src.models.user import TokenBlackListCreate, TokenBlackListUpdate, TokenBlackList


class TokenBlackList(CRUDBase[TokenBlackList, TokenBlackListCreate, TokenBlackListUpdate]):
   async def blacklist_create(self, db: AsyncSession, *, obj_in: TokenBlackListCreate, user_id: int) -> TokenBlackList:
    db_obj = TokenBlackList(
     email = onj_in.email,
     password = get_password_hash(obj_in.password),
     full_name = obj_in.full_name,
     blacklist_created_at = datetime.now(),
     is_active = True,
    )
    return await super().blacklist_create(db, obj_in=db_obj)
   
async def remove(self, db: AsyncSession, *, id: int) -> TokenBlackList:
    obj = await db.get(TokenBlackList, id)
    db.delete(obj)
    await db.commit()
    return obj

token_blacklist = TokenBlackList(TokenBlackList)
