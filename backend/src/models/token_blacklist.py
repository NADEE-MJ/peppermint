from datetime import datetime

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel


class TokenBlacklistBase(SQLModel):
    token: str



# Properties to receive via API on creation
class TokenBlacklistCreate(UserBase):
   pass


# Properties to receive via API on update
class TokenBlacklist(TokenBlacklistBase, table = True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime
    user_id: int = Field(foreign_key="user.id")


# Additional properties to return via API
class TokenBlacklistReponse(TokenBlacklistBase):
    success: bool