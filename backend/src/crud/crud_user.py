from datetime import datetime
from math import ceil
from typing import Any, Dict, Optional

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.core.security import get_password_hash, verify_password
from src.crud.base import CRUDBase
from src.models.user import User, UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def get_all(self, db: AsyncSession, *, page: int = 0, limit: int = 100) -> dict[str, int | list[User]]:
        if limit == -1:
            paginated_results = (await db.execute(select(User).filter(User.is_admin == False))).scalars().all()  # noqa
            return {"paginated_results": paginated_results, "total_pages": 1}
        page *= limit
        paginated_results = (
            (await db.execute(select(User).filter(User.is_admin == False).offset(page).limit(limit)))  # noqa
            .scalars()
            .all()
        )

        count = (await db.execute(select(func.count(User.id)).filter(User.is_admin == False))).scalars().first()  # noqa
        if count is not None:
            total_pages = ceil(count / limit)
        else:
            total_pages = 0

        return {"paginated_results": paginated_results, "total_pages": total_pages}

    async def create(self, db: AsyncSession, *, is_admin: bool = False, obj_in: UserCreate) -> User:  # type: ignore
        db_obj = User(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            created_at=datetime.now(),
            is_active=True,
            is_admin=is_admin,
        )
        return await super().create(db, obj_in=db_obj)

    async def update(self, db: AsyncSession, *, db_obj: User, obj_in: UserUpdate | Dict[str, Any]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data and update_data["password"] is not None:
            hashed_password = get_password_hash(update_data["password"])
            update_data["password"] = hashed_password
        elif "password" in update_data:
            del update_data["password"]
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> Optional[User]:
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_admin(self, user: User) -> bool:
        return user.is_admin


user = CRUDUser(User)
