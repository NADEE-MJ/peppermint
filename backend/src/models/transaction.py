from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class TransactionBase(SQLModel):
    amount: float
    date: str
    desc: str


# Properties to receive via API on creation
class TransactionCreate(TransactionBase):
    pass


class ParseCSV(SQLModel):
    mapping: dict[str, str]
    file: str


# Properties to receive via API on update
class TransactionUpdate(BaseModel):
    amount: float | None = None
    desc: str | None = None
    date: str | None = None


class Transaction(SQLModel, table=True):
    id: int = Field(primary_key=True)
    amount: float
    date: datetime
    desc: str
    created_at: datetime
    user_id: int = Field(foreign_key="user.id")
    budget_id: int = Field(foreign_key="budget.id")
    category_id: int = Field(foreign_key="category.id")
    account_id: int = Field(foreign_key="account.id")


# Additional properties to return via API
class TransactionResponse(SQLModel):
    id: int
    user_id: int
    budget_id: int
    category_id: int
    account_id: int
    created_at: datetime
    date: datetime
    amount: float
    desc: str
