"""
backend/models/workout_plan.py
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship

from backend.database.session import Base
from backend.models.enums import DifficultyLevel
from backend.models.mixins import TimestampMixin


class WorkoutPlan(Base, TimestampMixin):
    """
    A named workout program (e.g. "8-Week Strength Foundation")
    authored by a trainer. Its exercise list lives in
    WorkoutExercise; it gets handed out to members via MemberWorkout.
    """

    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Nullable: if a trainer account is removed, their plans stay on
    # record (unassigned) rather than disappearing.
    trainer_id = Column(
        Integer, ForeignKey("trainers.id", ondelete="SET NULL"), nullable=True, index=True
    )

    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    difficulty_level = Column(
        SAEnum(DifficultyLevel, name="workout_plan_difficulty_level"),
        nullable=False,
        default=DifficultyLevel.BEGINNER,
    )
    duration_weeks = Column(Integer, nullable=True)

    trainer = relationship("Trainer", back_populates="workout_plans")
    workout_exercises = relationship(
        "WorkoutExercise",
        back_populates="workout_plan",
        cascade="all, delete-orphan",
        order_by="WorkoutExercise.order_index",
    )
    member_workouts = relationship("MemberWorkout", back_populates="workout_plan")

    def __repr__(self) -> str:
        return f"<WorkoutPlan id={self.id} name={self.name!r}>"