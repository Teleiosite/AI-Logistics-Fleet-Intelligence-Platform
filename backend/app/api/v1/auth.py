from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.dependencies import AuthContext, get_auth_context
from app.core.rate_limit import RateLimitRule, get_client_key, rate_limiter
from app.core.security import (
    InvalidTokenError,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_password,
    verify_password,
)
from app.db.session import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserContextResponse
from app.services.crud import create_user, get_user_by_email

router = APIRouter(prefix="/auth", tags=["auth"])


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, request: Request, db: Session = Depends(get_db)) -> TokenResponse:
    settings = get_settings()
    rate_limiter.check(
        get_client_key(request, "register"),
        RateLimitRule(requests=settings.auth_rate_limit_requests, window_seconds=settings.auth_rate_limit_window_seconds),
    )
    password_hash = hash_password(payload.password)
    try:
        user = create_user(db, payload, password_hash=password_hash)
    except IntegrityError as exc:
        raise HTTPException(status_code=400, detail="Email already exists") from exc

    access_token = create_access_token(user.email, user.company_id, user.role)
    refresh_token = create_refresh_token(user.email, user.company_id, user.role)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)) -> TokenResponse:
    settings = get_settings()
    rate_limiter.check(
        get_client_key(request, "login"),
        RateLimitRule(requests=settings.auth_rate_limit_requests, window_seconds=settings.auth_rate_limit_window_seconds),
    )
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user.email, user.company_id, user.role)
    refresh_token = create_refresh_token(user.email, user.company_id, user.role)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest) -> TokenResponse:
    try:
        data = decode_refresh_token(payload.refresh_token)
    except InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    access_token = create_access_token(data["sub"], data["company_id"], data["role"])
    refresh_token = create_refresh_token(data["sub"], data["company_id"], data["role"])
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.get("/me", response_model=UserContextResponse)
def me(auth: AuthContext = Depends(get_auth_context)) -> UserContextResponse:
    return UserContextResponse(email=auth.email, company_id=auth.company_id, role=auth.role)
