"""
backend/models/member_workout.py
"""

from sqlalchemy import Column, Date, ForeignKey, Integer
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship

from backend.database.session import Base
from backend.models.enums import MemberWorkoutStatus
from backend.models.mixins import TimestampMixin


class MemberWorkout(Base, TimestampMixin):
    """
    Join table between Member and WorkoutPlan (many-to-many), with
    assignment metadata: who assigned it, when it started/ends, and
    its current status. A member can have several of these over time,
    or concurrently.
    """

    __tablename__ = "member_workouts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(
        Integer, ForeignKey("members.id", ondelete="CASCADE"), nullable=False, index=True
    )
    workout_plan_id = Column(
        Integer, ForeignKey("workout_plans.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assigned_by_trainer_id = Column(
        Integer, ForeignKey("trainers.id", ondelete="SET NULL"), nullable=True, index=True
    )

    status = Column(
        SAEnum(MemberWorkoutStatus, name="member_workout_status"),
        nullable=False,
        default=MemberWorkoutStatus.ACTIVE,
    )
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)

    member = relationship("Member", back_populates="member_workouts")
    workout_plan = relationship("WorkoutPlan", back_populates="member_workouts")
    assigned_by_trainer = relationship("Trainer")
    workout_logs = relationship("WorkoutLog", back_populates="member_workout")

    def __repr__(self) -> str:
        return (
            f"<MemberWorkout member={self.member_id} "
            f"plan={self.workout_plan_id} status={self.status}>"
        )