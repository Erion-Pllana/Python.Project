"""
backend/models/announcement.py
"""

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship

from backend.database.session import Base
from backend.models.enums import AnnouncementAudience
from backend.models.mixins import TimestampMixin


class Announcement(Base, TimestampMixin):
    """
    Gym-wide (or role-targeted) announcement posted by an admin or
    trainer, e.g. "Pool closed for maintenance this weekend".
    """

    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Nullable + SET NULL: if the author's account is later removed,
    # the announcement itself stays on record.
    created_by = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )

    title = Column(String(150), nullable=False)
    content = Column(Text, nullable=False)
    target_audience = Column(
        SAEnum(AnnouncementAudience, name="announcement_audience"),
        nullable=False,
        default=AnnouncementAudience.ALL,
    )
    is_active = Column(Boolean, nullable=False, default=True)
    published_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    created_by_user = relationship("User", back_populates="announcements")

    def __repr__(self) -> str:
        return f"<Announcement id={self.id} title={self.title!r}>"