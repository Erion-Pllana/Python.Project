"""
backend/schemas/workout_log.py
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class WorkoutLogBase(BaseModel):
    log_date: date
    sets_completed: Optional[int] = Field(None, ge=0)
    reps_completed: Optional[int] = Field(None, ge=0)
    weight_used_kg: Optional[Decimal] = Field(None, max_digits=6, decimal_places=2)
    duration_seconds: Optional[int] = Field(None, ge=0)
    calories_burned: Optional[Decimal] = Field(None, max_digits=6, decimal_places=2)
    notes: Optional[str] = None


class WorkoutLogCreate(WorkoutLogBase):
    member_id: int
    exercise_id: int
    member_workout_id: Optional[int] = None


class WorkoutLogUpdate(BaseModel):
    sets_completed: Optional[int] = None
    reps_completed: Optional[int] = None
    weight_used_kg: Optional[Decimal] = None
    duration_seconds: Optional[int] = None
    calories_burned: Optional[Decimal] = None
    notes: Optional[str] = None


class WorkoutLogRead(WorkoutLogBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: int
    exercise_id: int
    member_workout_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime