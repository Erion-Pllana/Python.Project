"""
backend/schemas/auth.py

Pydantic request/response models used by authentication endpoints.
"""

from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)

from backend.models.enums import UserRole
from backend.schemas.member import MemberRead
from backend.schemas.trainer import TrainerRead


class RegisterRequest(BaseModel):
    """Public self-registration. New public accounts are always MEMBERs."""

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )

    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    phone: Optional[str] = Field(
        None,
        max_length=20,
    )

    @field_validator(
        "username",
        "first_name",
        "last_name",
    )
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "This field cannot be blank."
            )

        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if value != value.strip():
            raise ValueError(
                "Password cannot start or end with whitespace."
            )

        if len(value) < 8:
            raise ValueError(
                "Password must be at least 8 characters long."
            )

        return value

    @field_validator("phone")
    @classmethod
    def strip_phone(
        cls,
        value: Optional[str],
    ) -> Optional[str]:
        return value.strip() if value and value.strip() else None


class LoginRequest(BaseModel):
    """Login with either a username or an email, plus password."""

    username_or_email: str = Field(
        ...,
        min_length=1,
    )

    password: str = Field(
        ...,
        min_length=1,
    )

    @field_validator("username_or_email")
    @classmethod
    def strip_identifier(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "Username or email is required."
            )

        return value


class ChangePasswordRequest(BaseModel):
    """Change the password of the currently authenticated account."""

    current_password: str = Field(
        ...,
        min_length=1,
        max_length=128,
    )

    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, value: str) -> str:
        if value != value.strip():
            raise ValueError(
                "Password cannot start or end with whitespace."
            )

        if len(value) < 8:
            raise ValueError(
                "New password must be at least 8 characters long."
            )

        return value


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CurrentUserRead(BaseModel):
    """Authenticated account plus its role-specific profile."""

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    username: str
    email: EmailStr
    role: UserRole
    is_active: bool

    member_profile: Optional[MemberRead] = None
    trainer_profile: Optional[TrainerRead] = None