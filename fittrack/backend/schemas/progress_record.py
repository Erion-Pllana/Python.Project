"""
backend/schemas/progress_record.py
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProgressRecordBase(BaseModel):
    record_date: date
    weight_kg: Optional[Decimal] = Field(None, max_digits=5, decimal_places=2)
    body_fat_percentage: Optional[Decimal] = Field(None, max_digits=4, decimal_places=2)
    muscle_mass_kg: Optional[Decimal] = Field(None, max_digits=5, decimal_places=2)
    chest_cm: Optional[Decimal] = Field(None, max_digits=5, decimal_places=2)
    waist_cm: Optional[Decimal] = Field(None, max_digits=5, decimal_places=2)
    hips_cm: Optional[Decimal] = Field(None, max_digits=5, decimal_places=2)
    notes: Optional[str] = None


class ProgressRecordCreate(ProgressRecordBase):
    member_id: int
    recorded_by_trainer_id: Optional[int] = None


class ProgressRecordUpdate(BaseModel):
    weight_kg: Optional[Decimal] = None
    body_fat_percentage: Optional[Decimal] = None
    muscle_mass_kg: Optional[Decimal] = None
    chest_cm: Optional[Decimal] = None
    waist_cm: Optional[Decimal] = None
    hips_cm: Optional[Decimal] = None
    notes: Optional[str] = None


class ProgressRecordRead(ProgressRecordBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: int
    recorded_by_trainer_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime