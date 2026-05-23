from __future__ import annotations

from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import TokenPair, UserCreate


def normalize_email(email: str) -> str:
    return email.strip().lower()


def create_user(session: Session, payload: UserCreate, is_superuser: bool = False) -> User:
    email = normalize_email(payload.email)
    existing_user = session.scalar(select(User).where(User.email == email))
    if existing_user is not None:
        raise ValueError("Email already registered")

    user = User(
        email=email,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
        is_superuser=is_superuser,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    user = session.scalar(select(User).where(User.email == normalize_email(email)))
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def issue_token_pair(session: Session, user: User) -> TokenPair:
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))
    user.refresh_token_hash = hash_password(refresh_token)
    session.add(user)
    session.commit()
    session.refresh(user)

    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=user,
    )


def refresh_token_pair(session: Session, refresh_token: str) -> TokenPair:
    from app.core.security import decode_token

    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
        raise ValueError("Invalid refresh token")

    subject = payload.get("sub")
    if not subject:
        raise ValueError("Invalid refresh token")

    user = session.get(User, int(subject))
    if user is None or not user.refresh_token_hash:
        raise ValueError("Invalid refresh token")
    if not verify_password(refresh_token, user.refresh_token_hash):
        raise ValueError("Invalid refresh token")

    return issue_token_pair(session, user)


def revoke_refresh_token(session: Session, user: User) -> None:
    user.refresh_token_hash = None
    session.add(user)
    session.commit()


def bootstrap_admin_user(session: Session) -> User | None:
    if not settings.ADMIN_BOOTSTRAP_EMAIL or not settings.ADMIN_BOOTSTRAP_PASSWORD:
        return None

    existing_user = session.scalar(select(User).limit(1))
    if existing_user is not None:
        return existing_user

    bootstrap_payload = UserCreate(
        email=settings.ADMIN_BOOTSTRAP_EMAIL,
        password=settings.ADMIN_BOOTSTRAP_PASSWORD,
        full_name=settings.ADMIN_BOOTSTRAP_NAME,
    )
    return create_user(session, bootstrap_payload, is_superuser=True)
