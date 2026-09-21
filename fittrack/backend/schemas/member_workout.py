"""
backend/schemas/member_workout.py
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from backend.models.enums import MemberWorkoutStatus


class MemberWorkoutBase(BaseModel):
    status: MemberWorkoutStatus = MemberWorkoutStatus.ACTIVE
    start_date: date
    end_date: Optional[date] = None


class MemberWorkoutCreate(MemberWorkoutBase):
    member_id: int
    workout_plan_id: int
    assigned_by_trainer_id: Optional[int] = None


class MemberWorkoutUpdate(BaseModel):
    status: Optional[MemberWorkoutStatus] = None
    end_date: Optional[date] = None


class MemberWorkoutRead(MemberWorkoutBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: int
    workout_plan_id: int
    assigned_by_trainer_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime