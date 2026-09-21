"""
backend/routers/auth.py

POST /api/auth/register     -- public self-registration (always MEMBER)
POST /api/auth/login        -- JSON login, used by Streamlit
POST /api/auth/login/form   -- OAuth2 form login, used by Swagger's "Authorize" button
GET  /api/auth/me           -- current authenticated user + their profile
"""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.models.user import User
from backend.schemas.auth import CurrentUserRead, LoginRequest, RegisterRequest, Token
from backend.security.dependencies import get_current_user
from backend.security.security import create_access_token
from backend.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=CurrentUserRead, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user = auth_service.register_member(db, payload)
    return _to_current_user_read(user)


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, payload.username_or_email, payload.password)
    token = create_access_token(subject=str(user.id))
    return Token(access_token=token)


@router.post("/login/form", response_model=Token, include_in_schema=False)
def login_via_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Identical to /login but accepts OAuth2's form body (Swagger UI's "Authorize" button)."""
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    token = create_access_token(subject=str(user.id))
    return Token(access_token=token)


@router.get("/me", response_model=CurrentUserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return _to_current_user_read(current_user)


def _to_current_user_read(user: User) -> CurrentUserRead:
    return CurrentUserRead(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
        member_profile=user.member,
        trainer_profile=user.trainer,
    )