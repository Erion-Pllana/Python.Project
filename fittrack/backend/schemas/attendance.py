"""
backend/schemas/attendance.py
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AttendanceBase(BaseModel):
    attendance_date: date
    check_in_time: datetime
    check_out_time: Optional[datetime] = None


class AttendanceCreate(AttendanceBase):
    member_id: int


class AttendanceUpdate(BaseModel):
    check_out_time: Optional[datetime] = None


class AttendanceRead(AttendanceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: int
    created_at: datetime
    updated_at: datetime