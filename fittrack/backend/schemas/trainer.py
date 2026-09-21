"""
backend/schemas/trainer.py
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TrainerBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    specialization: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = None
    hire_date: date


class TrainerCreate(TrainerBase):
    user_id: int


class TrainerUpdate(BaseModel):
    phone: Optional[str] = None
    specialization: Optional[str] = None
    bio: Optional[str] = None


class TrainerRead(TrainerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime