from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class TransactionBase(SQLModel):
    amount: float
    date: datetime
    desc: str


# Properties to receive via API on creation
class TransactionCreate(TransactionBase):
    pass


# Properties to receive via API on update
class TransactionUpdate(BaseModel):
    amount: float | None = None
    desc: str | None = None
    date: datetime | None = None


class Transaction(TransactionBase, table=True):
    id: int = Field(primary_key=True)
    created_at: datetime
    user_id: int = Field(foreign_key="user.id")
    budget_id: int = Field(foreign_key="budget.id")
    category_id: int = Field(foreign_key="category.id")


# Additional properties to return via API
class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    budget_id: int
    category_id: int
    created_at: datetime
