"""
backend/services/auth_service.py

Business logic for registration and login. Routers stay thin (HTTP
request/response concerns only) -- the actual rules live here.
"""

from datetime import date
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.models.enums import UserRole
from backend.models.member import Member
from backend.models.user import User
from backend.schemas.auth import RegisterRequest
from backend.security.security import hash_password, verify_password


def get_user_by_username_or_email(db: Session, identifier: str) -> Optional[User]:
    return (
        db.query(User)
        .filter(or_(User.username == identifier, User.email == identifier))
        .first()
    )


def register_member(db: Session, payload: RegisterRequest) -> User:
    """
    Create a new MEMBER account: a User row plus its Member profile
    row, together. Rejects a duplicate username or email with 409.
    """
    existing = get_user_by_username_or_email(
        db, payload.username
    ) or get_user_by_username_or_email(db, payload.email)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with that username or email already exists.",
        )

    user = User(
        username=payload.username,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=UserRole.MEMBER,
        is_active=True,
    )
    db.add(user)
    db.flush()  # populates user.id before we create the dependent Member row

    member = Member(
        user_id=user.id,
        first_name=payload.first_name,
        last_name=payload.last_name,
        phone=payload.phone,
        join_date=date.today(),
    )
    db.add(member)

    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username_or_email: str, password: str) -> User:
    """
    Verify credentials.

    Raises the *same* 401 for "no such user" and "wrong password" --
    distinguishing them would let a client use the error to enumerate
    which usernames/emails are registered.
    """
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username/email or password.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = get_user_by_username_or_email(db, username_or_email)
    if user is None or not verify_password(password, user.password_hash):
        raise unauthorized

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated.",
        )

    return user