"""
backend/schemas/workout_plan.py
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from backend.models.enums import DifficultyLevel


class WorkoutPlanBase(BaseModel):
    name: str = Field(..., max_length=150)
    description: Optional[str] = None
    difficulty_level: DifficultyLevel = DifficultyLevel.BEGINNER
    duration_weeks: Optional[int] = Field(None, ge=1, le=104)


class WorkoutPlanCreate(WorkoutPlanBase):
    trainer_id: Optional[int] = None


class WorkoutPlanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    difficulty_level: Optional[DifficultyLevel] = None
    duration_weeks: Optional[int] = None


class WorkoutPlanRead(WorkoutPlanBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    trainer_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime