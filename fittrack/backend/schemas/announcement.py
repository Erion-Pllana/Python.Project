"""
backend/schemas/announcement.py
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from backend.models.enums import AnnouncementAudience


class AnnouncementBase(BaseModel):
    title: str = Field(..., max_length=150)
    content: str
    target_audience: AnnouncementAudience = AnnouncementAudience.ALL
    is_active: bool = True
    published_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None


class AnnouncementCreate(AnnouncementBase):
    created_by: Optional[int] = None


class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None


class AnnouncementRead(AnnouncementBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime