"""
backend/security/dependencies.py

Reusable authentication and role-based authorization dependencies.
Role and active status are always read from the database, never trusted from
client-provided data or JWT claims.
"""

from typing import Optional

from fastapi import (
    Depends,
    HTTPException,
    status,
)

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.models.enums import UserRole
from backend.models.user import User
from backend.security.security import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login/form",
    auto_error=False,
)


def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:

    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )

    if token is None:
        raise credentials_error

    user_id = decode_access_token(token)

    if user_id is None:
        raise credentials_error

    try:
        user = db.get(
            User,
            int(user_id),
        )
    except (TypeError, ValueError):
        raise credentials_error

    if user is None or not user.is_active:
        raise credentials_error

    return user


def require_roles(*allowed_roles: UserRole):
    """Return a dependency that permits only the supplied roles."""

    allowed = set(allowed_roles)

    def _dependency(
        current_user: User = Depends(get_current_user),
    ) -> User:

        if current_user.role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )

        return current_user

    return _dependency


get_current_active_user = get_current_user

require_admin = require_roles(
    UserRole.ADMIN
)

require_trainer_or_admin = require_roles(
    UserRole.TRAINER,
    UserRole.ADMIN,
)

require_member = require_roles(
    UserRole.MEMBER
)