from datetime import datetime

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel
from enum import Enum


class types(str, Enum):
    savings = "savings"
    checking = "checking"
    credit = "credit"


class AccountBase(SQLModel):
    email: EmailStr


class AccountLogin(AccountBase):
    password: str


# Properties to receive via API on creation
class AccountCreate(AccountBase):
    password: str
    full_name: str | None = None


# Properties to receive via API on update
class AccountUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    full_name: str | None = None
    is_active: bool | None = None


class Account(AccountBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    created_at: datetime
    type: types
    name: str


# Additional properties to return via API
class AccountResponse(AccountBase):
    id: int
    full_name: str
    created_at: datetime
    last_login: datetime | None = None
    is_active: bool
