from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud
from src.api import deps
from src.core import security
from src.core.config import settings
from src.db.db import get_session
from src.models.json_msg import JsonMsgSuccess
from src.models.token import Token
from src.models.token import TokenBlacklistReponse
from src.models.user import User, UserResponse
from src.utils import (
    generate_magic_link_token,
    send_magic_link_email,
    verify_magic_link_token,
)

router = APIRouter()


@router.post("/login/access-token", response_model=Token)
async def login_access_token(
    login_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud.user.authenticate(db, email=login_data.username, password=login_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"email": user.email, "id": user.id}
    access_token: str = security.create_access_token(payload, expires_delta=access_token_expires)
    return {"access_token": access_token}


@router.post("/login/test-token", response_model=UserResponse)
def test_token(current_user: User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/send-magic-link", response_model=JsonMsgSuccess)
async def send_magic_link(email: EmailStr, db: AsyncSession = Depends(get_session)) -> Any:
    """
    Send a magic link to login
    """
    user = await crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    magic_link_token = generate_magic_link_token(email=email)
    send_magic_link_email(email=email, token=magic_link_token)
    return {"message": "Magic Link Sent", "success": True}


@router.post("/magic-link", response_model=Token)
async def magic_link(
    token: str,
    db: AsyncSession = Depends(get_session),
) -> Any:
    """
    Login user with magic link
    """
    email = verify_magic_link_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = await crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"email": user.email, "id": user.id}
    access_token: str = security.create_access_token(payload, expires_delta=access_token_expires)
    return {"access_token": access_token}
