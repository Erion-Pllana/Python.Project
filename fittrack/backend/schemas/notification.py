"""
backend/schemas/notification.py
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from backend.models.enums import NotificationType


class NotificationBase(BaseModel):
    title: str = Field(..., max_length=150)
    message: str
    notification_type: NotificationType = NotificationType.INFO
    is_read: bool = False


class NotificationCreate(NotificationBase):
    user_id: int


class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None


class NotificationRead(NotificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime