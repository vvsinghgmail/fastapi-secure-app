from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    content: str
    is_published: bool = False


class BlogCreate(BlogBase):
    pass


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None


class BlogRead(BlogBase):
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int

    class Config:
        from_attributes = True
