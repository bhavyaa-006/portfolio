from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.auth import RefreshRequest, TokenPair, UserCreate, UserRead
from app.services.auth_service import (
    authenticate_user,
    create_user,
    issue_token_pair,
    refresh_token_pair,
    revoke_refresh_token,
)
from app.utils.dependencies import get_current_active_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, session: Session = Depends(get_db)) -> UserRead:
    try:
        user = create_user(session, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return user


@router.post("/login/access-token", response_model=TokenPair)
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db),
) -> TokenPair:
    user = authenticate_user(session, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return issue_token_pair(session, user)


@router.post("/refresh", response_model=TokenPair)
def refresh_tokens(payload: RefreshRequest, session: Session = Depends(get_db)) -> TokenPair:
    try:
        return refresh_token_pair(session, payload.refresh_token)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.get("/me", response_model=UserRead)
def read_current_user(user=Depends(get_current_active_user)) -> UserRead:
    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout_current_user(user=Depends(get_current_active_user), session: Session = Depends(get_db)) -> None:
    revoke_refresh_token(session, user)
