from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from sqlmodel import Field, SQLModel, ForeignKey, Relationship

from src.models.user import User


class Types(str, Enum):
    savings = "savings"
    checking = "checking"
    credit = "credit"


class AccountBase(SQLModel):
    name: str


# Properties to receive via API on creation
class AccountCreate(AccountBase):
    account_type: Types


# Properties to receive via API on update
class AccountUpdate(BaseModel):
    account_type: Types | None = None
    name: str | None = None


class Account(AccountBase, table=True):
    id: int = Field(primary_key=True)
    created_at: datetime
    account_type: Types
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="accounts")


# Additional properties to return via API
class AccountResponse(AccountBase):
    id: int
    user_id: int
    account_type: Types
    created_at: datetime
