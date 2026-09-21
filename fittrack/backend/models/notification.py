"""
backend/models/notification.py
"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship

from backend.database.session import Base
from backend.models.enums import NotificationType
from backend.models.mixins import TimestampMixin


class Notification(Base, TimestampMixin):
    """
    A single in-app notification delivered to one user -- a payment
    reminder, a newly assigned workout, a posted announcement, etc.
    """

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    title = Column(String(150), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(
        SAEnum(NotificationType, name="notification_type"),
        nullable=False,
        default=NotificationType.INFO,
    )
    is_read = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="notifications")

    def __repr__(self) -> str:
        return f"<Notification id={self.id} user={self.user_id} type={self.notification_type}>"