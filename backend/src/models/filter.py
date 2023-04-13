from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class FilterBase(SQLModel):
    filter_by: str


# Properties to receive via API on creation
class FilterCreate(FilterBase):
    pass


# Properties to receive via API on update
class FilterUpdate(BaseModel):
    filter_by: str | None = None


class Filter(FilterBase, table=True):
    id: int = Field(primary_key=True)
    created_at: datetime
    user_id: int = Field(foreign_key="user.id")
    category_id: int = Field(foreign_key="category.id")


# Additional properties to return via API
class FilterResponse(FilterBase):
    id: int
    user_id: int
    category_id: int
    created_at: datetime
