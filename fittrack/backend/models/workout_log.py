"""
backend/models/workout_log.py
"""

from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import relationship

from backend.database.session import Base
from backend.models.mixins import TimestampMixin


class WorkoutLog(Base, TimestampMixin):
    """
    A single completed exercise, logged by a member -- optionally tied
    back to an assigned MemberWorkout, but not required to be (members
    can log ad-hoc exercise too). This is the actual performance data
    that progress charts and history are built from.
    """

    __tablename__ = "workout_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(
        Integer, ForeignKey("members.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # RESTRICT: historical logs must keep pointing at a real exercise.
    exercise_id = Column(
        Integer, ForeignKey("exercises.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    member_workout_id = Column(
        Integer,
        ForeignKey("member_workouts.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    log_date = Column(Date, nullable=False, index=True)
    sets_completed = Column(Integer, nullable=True)
    reps_completed = Column(Integer, nullable=True)
    weight_used_kg = Column(Numeric(6, 2), nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    calories_burned = Column(Numeric(6, 2), nullable=True)
    notes = Column(Text, nullable=True)

    member = relationship("Member", back_populates="workout_logs")
    exercise = relationship("Exercise", back_populates="workout_logs")
    member_workout = relationship("MemberWorkout", back_populates="workout_logs")

    def __repr__(self) -> str:
        return f"<WorkoutLog member={self.member_id} exercise={self.exercise_id} date={self.log_date}>"