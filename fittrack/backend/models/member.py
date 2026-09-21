"""
backend/models/member.py
"""

from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship

from backend.database.session import Base
from backend.models.enums import Gender
from backend.models.mixins import TimestampMixin


class Member(Base, TimestampMixin):
    """
    Gym-member profile, one-to-one with User (user_id is unique).
    Everything member-specific -- memberships, payments, attendance,
    assigned workouts, logged workouts, progress -- hangs off this
    table's id, not off users.id directly.
    """

    __tablename__ = "members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(SAEnum(Gender, name="gender"), nullable=True)
    address = Column(String(255), nullable=True)
    emergency_contact_name = Column(String(100), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)
    join_date = Column(Date, nullable=False)

    user = relationship("User", back_populates="member")

    memberships = relationship(
        "Membership", back_populates="member", cascade="all, delete-orphan"
    )
    payments = relationship(
        "Payment", back_populates="member", cascade="all, delete-orphan"
    )
    attendance_records = relationship(
        "Attendance", back_populates="member", cascade="all, delete-orphan"
    )
    member_workouts = relationship(
        "MemberWorkout", back_populates="member", cascade="all, delete-orphan"
    )
    workout_logs = relationship(
        "WorkoutLog", back_populates="member", cascade="all, delete-orphan"
    )
    progress_records = relationship(
        "ProgressRecord", back_populates="member", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Member id={self.id} name='{self.first_name} {self.last_name}'>"