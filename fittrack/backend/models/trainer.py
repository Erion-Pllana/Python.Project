"""
backend/models/trainer.py
"""

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.database.session import Base
from backend.models.mixins import TimestampMixin


class Trainer(Base, TimestampMixin):
    """
    Trainer profile, one-to-one with User. Trainers author WorkoutPlans
    that later get assigned to members.
    """

    __tablename__ = "trainers"

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
    specialization = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    hire_date = Column(Date, nullable=False)

    user = relationship("User", back_populates="trainer")
    workout_plans = relationship("WorkoutPlan", back_populates="trainer")

    def __repr__(self) -> str:
        return f"<Trainer id={self.id} name='{self.first_name} {self.last_name}'>"