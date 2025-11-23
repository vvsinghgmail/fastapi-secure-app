from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.api.deps import get_db, get_current_user
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.models.user import User, UserRole
from app.models.token import RefreshToken
from app.schemas.user import UserCreate, UserRead
from app.schemas.auth import TokenPair

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    existing = db.exec(select(User).where(User.email == user_in.email)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=UserRole.user,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenPair)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    request: Request = None,
) -> TokenPair:
    user = db.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(subject=user.id, roles=[user.role])
    refresh_token = create_refresh_token(subject=user.id)

    payload = decode_token(refresh_token)
    rt = RefreshToken(
        token=refresh_token,
        user_id=user.id,
        jti=payload["jti"],
        user_agent=request.headers.get("user-agent") if request else None,
        ip_address=request.client.host if request and request.client else None,
    )
    db.add(rt)
    db.commit()
    return TokenPair(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenPair)
def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db),
    request: Request = None,
) -> TokenPair:
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    rt_db = db.exec(
        select(RefreshToken).where(
            RefreshToken.token == refresh_token,
            RefreshToken.revoked == False,  # noqa: E712
        )
    ).first()
    if not rt_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token revoked or not found",
        )

    rt_db.revoked = True
    db.add(rt_db)

    user_id = int(payload["sub"])
    user = db.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access = create_access_token(subject=user.id, roles=[user.role])
    new_refresh = create_refresh_token(subject=user.id)
    new_payload = decode_token(new_refresh)

    rt_new = RefreshToken(
        token=new_refresh,
        user_id=user.id,
        jti=new_payload["jti"],
        user_agent=request.headers.get("user-agent") if request else None,
        ip_address=request.client.host if request and request.client else None,
    )
    db.add(rt_new)
    db.commit()

    return TokenPair(access_token=new_access, refresh_token=new_refresh)


@router.post("/logout")
def logout(
    refresh_token: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rt_db = db.exec(
        select(RefreshToken).where(
            RefreshToken.token == refresh_token,
            RefreshToken.user_id == current_user.id,
            RefreshToken.revoked == False,  # noqa: E712
        )
    ).first()
    if not rt_db:
        raise HTTPException(status_code=404, detail="Refresh token not found")
    rt_db.revoked = True
    db.add(rt_db)
    db.commit()
    return {"detail": "Logged out from this session"}


@router.post("/logout-all")
def logout_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tokens = db.exec(
        select(RefreshToken).where(
            RefreshToken.user_id == current_user.id,
            RefreshToken.revoked == False,  # noqa: E712
        )
    ).all()
    for t in tokens:
        t.revoked = True
        db.add(t)
    db.commit()
    return {"detail": "Logged out from all sessions"}
