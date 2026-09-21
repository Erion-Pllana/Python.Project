"""
backend/models/workout_exercise.py
"""

from sqlalchemy import Column, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from backend.database.session import Base
from backend.models.mixins import TimestampMixin


class WorkoutExercise(Base, TimestampMixin):
    """
    Join table between WorkoutPlan and Exercise (many-to-many), with
    the prescription for that exercise inside that plan: order, sets,
    reps, rest, etc.
    """

    __tablename__ = "workout_exercises"
    __table_args__ = (
        UniqueConstraint(
            "workout_plan_id", "exercise_id", "order_index", name="uq_plan_exercise_order"
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    workout_plan_id = Column(
        Integer, ForeignKey("workout_plans.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # RESTRICT: an exercise that's used in a plan can't be deleted out
    # from under it -- retire it (or remove it from the plan) instead.
    exercise_id = Column(
        Integer, ForeignKey("exercises.id", ondelete="RESTRICT"), nullable=False, index=True
    )

    order_index = Column(Integer, nullable=False, default=1)
    sets = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    rest_seconds = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)

    workout_plan = relationship("WorkoutPlan", back_populates="workout_exercises")
    exercise = relationship("Exercise", back_populates="workout_exercises")

    def __repr__(self) -> str:
        return (
            f"<WorkoutExercise plan={self.workout_plan_id} "
            f"exercise={self.exercise_id} order={self.order_index}>"
        )