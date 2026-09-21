"""
backend/schemas/auth.py
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from backend.models.enums import UserRole
from backend.schemas.member import MemberRead
from backend.schemas.trainer import TrainerRead


class RegisterRequest(BaseModel):
    """
    Public self-registration. This always creates a MEMBER account --
    ADMIN and TRAINER accounts are created by an admin through the
    member-management CRUD (Step 4+), never through open registration.
    """

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    phone: Optional[str] = Field(None, max_length=20)


class LoginRequest(BaseModel):
    """Login with either a username or an email, plus password."""

    username_or_email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CurrentUserRead(BaseModel):
    """
    What GET /api/auth/me returns: account info plus whichever
    role-specific profile applies. At most one of member_profile /
    trainer_profile is set (an ADMIN has neither).
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    role: UserRole
    is_active: bool
    member_profile: Optional[MemberRead] = None
    trainer_profile: Optional[TrainerRead] = None