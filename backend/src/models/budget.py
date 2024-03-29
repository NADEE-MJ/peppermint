from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class BudgetBase(SQLModel):
    name: str


# Properties to receive via API on creation
class BudgetCreate(BudgetBase):
    amount: float


# Properties to receive via API on update
class BudgetUpdate(BaseModel):
    amount: float | None = None
    name: str | None = None


class Budget(BudgetBase, table=True):
    id: int = Field(primary_key=True)
    created_at: datetime
    amount: float
    user_id: int = Field(foreign_key="user.id")


# Additional properties to return via API
class BudgetResponse(BudgetBase):
    id: int
    user_id: int
    amount: float
    created_at: datetime
