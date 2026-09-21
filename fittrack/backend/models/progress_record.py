"""
backend/models/progress_record.py
"""

from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import relationship

from backend.database.session import Base
from backend.models.mixins import TimestampMixin


class ProgressRecord(Base, TimestampMixin):
    """
    A periodic body-measurement snapshot for a member (weight, body
    fat %, key measurements) -- what progress-over-time charts read
    from. Optionally recorded by a trainer rather than the member.
    """

    __tablename__ = "progress_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(
        Integer, ForeignKey("members.id", ondelete="CASCADE"), nullable=False, index=True
    )
    recorded_by_trainer_id = Column(
        Integer, ForeignKey("trainers.id", ondelete="SET NULL"), nullable=True, index=True
    )

    record_date = Column(Date, nullable=False, index=True)
    weight_kg = Column(Numeric(5, 2), nullable=True)
    body_fat_percentage = Column(Numeric(4, 2), nullable=True)
    muscle_mass_kg = Column(Numeric(5, 2), nullable=True)
    chest_cm = Column(Numeric(5, 2), nullable=True)
    waist_cm = Column(Numeric(5, 2), nullable=True)
    hips_cm = Column(Numeric(5, 2), nullable=True)
    notes = Column(Text, nullable=True)

    member = relationship("Member", back_populates="progress_records")
    recorded_by_trainer = relationship("Trainer")

    def __repr__(self) -> str:
        return f"<ProgressRecord member={self.member_id} date={self.record_date}>"