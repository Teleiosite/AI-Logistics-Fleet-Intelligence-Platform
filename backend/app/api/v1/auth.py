from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.dependencies import AuthContext, get_auth_context
from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserContextResponse
from app.services.crud import create_user, get_user_by_email

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> TokenResponse:
    password_hash = hash_password(payload.password)
    try:
        user = create_user(db, payload, password_hash=password_hash)
    except IntegrityError as exc:
        raise HTTPException(status_code=400, detail="Email already exists") from exc

    token = create_access_token(user.email, user.company_id, user.role)
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.email, user.company_id, user.role)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserContextResponse)
def me(auth: AuthContext = Depends(get_auth_context)) -> UserContextResponse:
    return UserContextResponse(email=auth.email, company_id=auth.company_id, role=auth.role)
