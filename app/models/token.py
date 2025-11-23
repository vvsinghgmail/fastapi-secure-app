from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field, Column, Integer, ForeignKey


class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"

    id: Optional[int] = Field(default=None, primary_key=True)
    token: str = Field(nullable=False, unique=True)  # in real prod, hash this
    user_id: int = Field(sa_column=Column(Integer, ForeignKey("users.id")))
    jti: str = Field(nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    revoked: bool = Field(default=False)
    user_agent: Optional[str] = Field(default=None)
    ip_address: Optional[str] = Field(default=None)
