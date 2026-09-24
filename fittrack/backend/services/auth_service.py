"""
backend/services/auth_service.py

Business logic for registration, login and password changes. Routers stay
thin and all database writes are rolled back when an unexpected error occurs.
"""

from datetime import date
from typing import Optional

from fastapi import (
    HTTPException,
    status,
)

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.models.enums import UserRole
from backend.models.member import Member
from backend.models.user import User

from backend.schemas.auth import (
    ChangePasswordRequest,
    RegisterRequest,
)

from backend.security.security import (
    hash_password,
    verify_password,
)


def get_user_by_username_or_email(
    db: Session,
    identifier: str,
) -> Optional[User]:

    identifier = identifier.strip()
    email_identifier = identifier.lower()

    return (
        db.query(User)
        .filter(
            or_(
                User.username == identifier,
                User.email == email_identifier,
            )
        )
        .first()
    )


def register_member(
    db: Session,
    payload: RegisterRequest,
) -> User:

    """Create a new MEMBER account and its one-to-one Member profile."""

    username = payload.username.strip()
    email = str(payload.email).strip().lower()

    existing = (
        db.query(User)
        .filter(
            or_(
                User.username == username,
                User.email == email,
            )
        )
        .first()
    )

    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with that username or email already exists.",
        )

    user = User(
        username=username,
        email=email,
        password_hash=hash_password(
            payload.password
        ),
        role=UserRole.MEMBER,
        is_active=True,
    )

    db.add(user)

    try:
        db.flush()

        db.add(
            Member(
                user_id=user.id,
                first_name=payload.first_name.strip(),
                last_name=payload.last_name.strip(),
                phone=payload.phone,
                join_date=date.today(),
            )
        )

        db.commit()
        db.refresh(user)

        return user

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with that username or email already exists.",
        )

    except Exception:
        db.rollback()
        raise


def authenticate_user(
    db: Session,
    username_or_email: str,
    password: str,
) -> User:

    """Verify credentials and return the active user."""

    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username/email or password.",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )

    user = get_user_by_username_or_email(
        db,
        username_or_email,
    )

    if user is None or not verify_password(
        password,
        user.password_hash,
    ):
        raise unauthorized

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated.",
        )

    return user


def change_password(
    db: Session,
    user: User,
    payload: ChangePasswordRequest,
) -> None:

    """Verify the current password and replace it with a new hash."""

    if not verify_password(
        payload.current_password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect.",
        )

    if payload.current_password == payload.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from the current password.",
        )

    user.password_hash = hash_password(
        payload.new_password
    )

    try:
        db.commit()

    except Exception:
        db.rollback()
        raise