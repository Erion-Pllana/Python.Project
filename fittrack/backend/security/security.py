"""
backend/security/security.py

Password hashing and JWT creation/verification.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Hash a plain-text password for storage. Never store plain text."""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Check a plain-text password against a stored bcrypt hash."""
    return pwd_context.verify(plain_password, password_hash)


def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    """
    Create a signed JWT access token.

    `subject` should be the user's id, as a string -- that's the only
    thing get_current_user() trusts from the token. Role and
    active-status are always re-read from the database on every
    request rather than taken from token claims.
    """
    expire_minutes = expires_minutes or settings.access_token_expire_minutes
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    to_encode: dict[str, Any] = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> Optional[str]:
    """
    Decode and verify a JWT. Returns the subject (user id, as a
    string) if the token is valid and unexpired, or None for any
    failure (bad signature, malformed token, expired token).
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        return None
    return payload.get("sub")