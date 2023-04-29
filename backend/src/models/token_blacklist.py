from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class TokenBlacklistBase(SQLModel):
    token: str


# Properties to receive on creation
class TokenBlacklistCreate(TokenBlacklistBase):
    pass


# Properties to receive on creation
class TokenBlacklistUpdate(BaseModel):
    pass


class TokenBlacklist(TokenBlacklistBase, table=True):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime
    user_id: int = Field(foreign_key="user.id")


class TokenBlacklistResponse(TokenBlacklistBase):
    success: bool
