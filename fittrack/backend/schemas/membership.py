"""
backend/schemas/membership.py
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from backend.models.enums import MembershipStatus, MembershipType


class MembershipBase(BaseModel):
    membership_type: MembershipType
    status: MembershipStatus = MembershipStatus.PENDING
    start_date: date
    end_date: date
    fee: Decimal = Field(..., max_digits=8, decimal_places=2)


class MembershipCreate(MembershipBase):
    member_id: int


class MembershipUpdate(BaseModel):
    status: Optional[MembershipStatus] = None
    end_date: Optional[date] = None


class MembershipRead(MembershipBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: int
    created_at: datetime
    updated_at: datetime