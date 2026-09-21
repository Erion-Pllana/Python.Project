"""
backend/models/exercise.py
"""

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship

from backend.database.session import Base
from backend.models.enums import DifficultyLevel, ExerciseCategory
from backend.models.mixins import TimestampMixin


class Exercise(Base, TimestampMixin):
    """
    Catalog of exercises available to build workout plans from (e.g.
    "Barbell Squat", "Treadmill Run"). Shared across all trainers --
    not owned by any one plan or member.
    """

    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(SAEnum(ExerciseCategory, name="exercise_category"), nullable=False)
    muscle_group = Column(String(100), nullable=True)
    equipment_needed = Column(String(150), nullable=True)
    difficulty_level = Column(
        SAEnum(DifficultyLevel, name="exercise_difficulty_level"),
        nullable=False,
        default=DifficultyLevel.BEGINNER,
    )

    workout_exercises = relationship("WorkoutExercise", back_populates="exercise")
    workout_logs = relationship("WorkoutLog", back_populates="exercise")

    def __repr__(self) -> str:
        return f"<Exercise id={self.id} name={self.name!r}>"