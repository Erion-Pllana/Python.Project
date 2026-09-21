"""
backend/security/dependencies.py

Reusable FastAPI dependencies for authentication and role-based
authorization. Every protected route depends on one of these instead
of re-implementing the check.

Critically: every one of these re-reads the user (and their role) from
the database on each request via get_current_user(). Nothing about who
someone is or what role they hold is ever taken on faith from the
client -- not from a request body, not even from the JWT's own claims
beyond the user id used to look the row up.
"""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.models.enums import UserRole
from backend.models.user import User
from backend.security.security import decode_access_token

# tokenUrl only tells Swagger's "Authorize" button where to POST a
# trial login -- it has no effect on how tokens are verified below.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login/form", auto_error=False)


def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Decode the bearer token, load the matching active user from the
    database, and return it.

    Raises 401 for every failure case -- missing token, malformed or
    expired token, a user id that no longer exists, or a deactivated
    account -- and deliberately doesn't distinguish which, so a client
    probing with a bad token can't learn which case applied.
    """
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if token is None:
        raise credentials_error

    user_id = decode_access_token(token)
    if user_id is None:
        raise credentials_error

    try:
        user = db.get(User, int(user_id))
    except (TypeError, ValueError):
        raise credentials_error

    if user is None or not user.is_active:
        raise credentials_error

    return user


def require_roles(*allowed_roles: UserRole):
    """
    Dependency factory: only lets the given roles through.

        Depends(require_roles(UserRole.ADMIN))
        Depends(require_roles(UserRole.TRAINER, UserRole.ADMIN))
    """

    def _dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )
        return current_user

    return _dependency


get_current_active_user = get_current_user
require_admin = require_roles(UserRole.ADMIN)
require_trainer_or_admin = require_roles(UserRole.TRAINER, UserRole.ADMIN)
require_member = require_roles(UserRole.MEMBER)