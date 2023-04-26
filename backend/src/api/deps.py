import json

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.core import security
from src.core.config import settings
from src.db.db import get_session
from src.models.token import TokenPayload
from src.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_VERSION_STR}/login/access-token")


async def get_current_user(
    db: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
) -> User:
    if not token:
        raise HTTPException(status_code=401, detail="Not Logged In")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await crud.user.get(db, id=json.loads(token_data.sub)["id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User | None:
    if current_user.is_admin:
        raise HTTPException(status_code=401, detail="Admin cannot access function")

    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_admin(
    current_user: User = Depends(get_current_user),
) -> User | None:
    if not current_user.is_admin:
        raise HTTPException(status_code=401, detail="Admins only allowed")

    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
