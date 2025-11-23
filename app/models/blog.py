from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship, Column, Integer, ForeignKey


class Blog(SQLModel, table=True):
    __tablename__ = "blogs"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, nullable=False)
    content: str = Field(nullable=False)
    is_published: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    owner_id: int = Field(sa_column=Column(Integer, ForeignKey("users.id")))
    owner: "User" = Relationship(back_populates="blogs")

