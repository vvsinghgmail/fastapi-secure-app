from datetime import datetime, timedelta, timezone
from typing import Any, Union, Optional, List
from uuid import uuid4

from passlib.context import CryptContext
from jose import jwt, JWTError

from app.core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: Union[str, Any], roles: List[str]) -> str:
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {
        "sub": str(subject),
        "roles": roles,
        "exp": expire,
        "type": "access",
        "jti": str(uuid4()),
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(subject: Union[str, Any]) -> str:
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "type": "refresh",
        "jti": str(uuid4()),
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    settings = get_settings()
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
