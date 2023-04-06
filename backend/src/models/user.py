from datetime import datetime

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: EmailStr


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str
    full_name: str | None = None


# Properties to receive via API on update
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    full_name: str | None = None
    is_active: bool | None = None


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str
    full_name: str
    created_at: datetime
    last_login: datetime | None = None
    is_active: bool


# Additional properties to return via API
class UserResponse(UserBase):
    id: int
    full_name: str
    created_at: datetime
    last_login: datetime | None = None
    is_active: bool
