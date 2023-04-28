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

    user_id = json.loads(token_data.sub)["id"]
    # check if token is blacklisted
    blacklisted_tokens = await crud.token_blacklist.get_all_tokens_for_user(db, user_id=user_id)

    if blacklisted_tokens:
        for blacklisted_token in blacklisted_tokens:
            if blacklisted_token.token == token:
                raise HTTPException(status_code=401, detail="Could not validate credentials: Token blacklisted")

    user = await crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User | None:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
