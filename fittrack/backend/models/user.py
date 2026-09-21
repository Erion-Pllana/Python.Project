"""
backend/models/user.py
"""

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship

from backend.database.session import Base
from backend.models.enums import UserRole
from backend.models.mixins import TimestampMixin


class User(Base, TimestampMixin):
    """
    Login account for FitTrack. Every person who can sign in -- admin,
    trainer, or member -- has exactly one row here. Role-specific
    profile data (name, phone, etc.) lives in Member / Trainer, linked
    1-to-1, not on this table.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(
        SAEnum(UserRole, name="user_role"),
        nullable=False,
        default=UserRole.MEMBER,
    )
    is_active = Column(Boolean, nullable=False, default=True)

    # 1-to-1 role profiles. Deleting a user cleans up their one profile.
    member = relationship(
        "Member", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    trainer = relationship(
        "Trainer", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    # Things this user receives or authored.
    notifications = relationship(
        "Notification", back_populates="user", cascade="all, delete-orphan"
    )
    announcements = relationship("Announcement", back_populates="created_by_user")

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r} role={self.role}>"