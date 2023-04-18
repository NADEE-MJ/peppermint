from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class CategoryBase(SQLModel):
    name: str


# Properties to receive via API on creation
class CategoryCreate(CategoryBase):
    desc: str


# Properties to receive via API on update
class CategoryUpdate(BaseModel):
    desc: str | None = None
    name: str | None = None


class Category(CategoryBase, table=True):
    id: int = Field(primary_key=True)
    created_at: datetime
    desc: str
    user_id: int = Field(foreign_key="user.id")
    budget_id: int = Field(foreign_key="budget.id")


# Additional properties to return via API
class CategoryResponse(CategoryBase):
    id: int
    user_id: int
    budget_id: int
    desc: str
    created_at: datetime
