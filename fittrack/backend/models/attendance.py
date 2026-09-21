"""
backend/models/attendance.py
"""

from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, Integer
from sqlalchemy.orm import relationship

from backend.database.session import Base
from backend.models.mixins import TimestampMixin


class Attendance(Base, TimestampMixin):
    """
    One row per gym visit: a check-in, with an optional check-out.
    """

    __tablename__ = "attendance"
    __table_args__ = (
        Index("ix_attendance_member_date", "member_id", "attendance_date"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(
        Integer, ForeignKey("members.id", ondelete="CASCADE"), nullable=False, index=True
    )

    attendance_date = Column(Date, nullable=False)
    check_in_time = Column(DateTime, nullable=False)
    check_out_time = Column(DateTime, nullable=True)

    member = relationship("Member", back_populates="attendance_records")

    def __repr__(self) -> str:
        return f"<Attendance member={self.member_id} date={self.attendance_date}>"