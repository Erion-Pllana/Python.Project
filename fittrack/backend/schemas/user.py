"""
backend/schemas/user.py
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from backend.models.enums import UserRole


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: UserRole = UserRole.MEMBER
    is_active: bool = True


class UserCreate(UserBase):
    """
    Used to register a new login account. The plain password comes in
    here and gets hashed before it's ever written to the database --
    that hashing happens in Step 4's auth logic, not in this schema.
    """

    password: str = Field(..., min_length=8, max_length=128)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime