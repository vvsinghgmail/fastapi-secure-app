from typing import Optional, List
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship


class UserRole(str, Enum):
    admin = "admin"
    user = "user"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str
    is_active: bool = Field(default=True)
    role: UserRole = Field(default=UserRole.user)

    blogs: List["Blog"] = Relationship(back_populates="owner")

