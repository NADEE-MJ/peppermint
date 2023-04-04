from datetime import datetime

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel
from enum import Enum


class Types(str, Enum):
    savings = "savings"
    checking = "checking"
    credit = "credit"


class AccountBase(SQLModel):
    name: str


# Properties to receive via API on creation
class AccountCreate(AccountBase):
    account_type: Types
    user_id: int


# Properties to receive via API on update
class AccountUpdate(BaseModel):
    account_type: Types | None = None
    name: Types | None = None


class Account(AccountBase, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime
    account_type: Types


# Additional properties to return via API
class AccountResponse(AccountBase):
    id: int
    user_id: int
    account_type: Types
    created_at: datetime
