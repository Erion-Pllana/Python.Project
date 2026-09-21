"""
backend/schemas/payment.py
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from backend.models.enums import PaymentMethod, PaymentStatus


class PaymentBase(BaseModel):
    amount: Decimal = Field(..., max_digits=8, decimal_places=2)
    payment_date: date
    payment_method: PaymentMethod
    status: PaymentStatus = PaymentStatus.PENDING
    transaction_reference: Optional[str] = Field(None, max_length=100)


class PaymentCreate(PaymentBase):
    member_id: int
    membership_id: Optional[int] = None


class PaymentUpdate(BaseModel):
    status: Optional[PaymentStatus] = None
    transaction_reference: Optional[str] = None


class PaymentRead(PaymentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: int
    membership_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime