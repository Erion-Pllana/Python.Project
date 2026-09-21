"""
backend/schemas/exercise.py
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from backend.models.enums import DifficultyLevel, ExerciseCategory


class ExerciseBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    category: ExerciseCategory
    muscle_group: Optional[str] = Field(None, max_length=100)
    equipment_needed: Optional[str] = Field(None, max_length=150)
    difficulty_level: DifficultyLevel = DifficultyLevel.BEGINNER


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseUpdate(BaseModel):
    description: Optional[str] = None
    muscle_group: Optional[str] = None
    equipment_needed: Optional[str] = None
    difficulty_level: Optional[DifficultyLevel] = None


class ExerciseRead(ExerciseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime