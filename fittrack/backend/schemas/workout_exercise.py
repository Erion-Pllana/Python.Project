"""
backend/schemas/workout_exercise.py
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class WorkoutExerciseBase(BaseModel):
    order_index: int = Field(1, ge=1)
    sets: Optional[int] = Field(None, ge=1)
    reps: Optional[int] = Field(None, ge=1)
    duration_seconds: Optional[int] = Field(None, ge=1)
    rest_seconds: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = None


class WorkoutExerciseCreate(WorkoutExerciseBase):
    workout_plan_id: int
    exercise_id: int


class WorkoutExerciseUpdate(BaseModel):
    order_index: Optional[int] = None
    sets: Optional[int] = None
    reps: Optional[int] = None
    duration_seconds: Optional[int] = None
    rest_seconds: Optional[int] = None
    notes: Optional[str] = None


class WorkoutExerciseRead(WorkoutExerciseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    workout_plan_id: int
    exercise_id: int
    created_at: datetime
    updated_at: datetime