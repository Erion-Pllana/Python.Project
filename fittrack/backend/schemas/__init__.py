"""
backend/schemas/__init__.py

Re-exports every schema so routers/services can do, e.g.:
    from backend.schemas import MemberCreate, MemberRead
instead of importing from each individual module.
"""

from backend.schemas.announcement import (
    AnnouncementBase,
    AnnouncementCreate,
    AnnouncementRead,
    AnnouncementUpdate,
)
from backend.schemas.attendance import (
    AttendanceBase,
    AttendanceCreate,
    AttendanceRead,
    AttendanceUpdate,
)
from backend.schemas.exercise import (
    ExerciseBase,
    ExerciseCreate,
    ExerciseRead,
    ExerciseUpdate,
)
from backend.schemas.member import MemberBase, MemberCreate, MemberRead, MemberUpdate
from backend.schemas.member_workout import (
    MemberWorkoutBase,
    MemberWorkoutCreate,
    MemberWorkoutRead,
    MemberWorkoutUpdate,
)
from backend.schemas.membership import (
    MembershipBase,
    MembershipCreate,
    MembershipRead,
    MembershipUpdate,
)
from backend.schemas.notification import (
    NotificationBase,
    NotificationCreate,
    NotificationRead,
    NotificationUpdate,
)
from backend.schemas.payment import PaymentBase, PaymentCreate, PaymentRead, PaymentUpdate
from backend.schemas.progress_record import (
    ProgressRecordBase,
    ProgressRecordCreate,
    ProgressRecordRead,
    ProgressRecordUpdate,
)
from backend.schemas.trainer import TrainerBase, TrainerCreate, TrainerRead, TrainerUpdate
from backend.schemas.user import UserBase, UserCreate, UserRead, UserUpdate
from backend.schemas.workout_exercise import (
    WorkoutExerciseBase,
    WorkoutExerciseCreate,
    WorkoutExerciseRead,
    WorkoutExerciseUpdate,
)
from backend.schemas.workout_log import (
    WorkoutLogBase,
    WorkoutLogCreate,
    WorkoutLogRead,
    WorkoutLogUpdate,
)
from backend.schemas.workout_plan import (
    WorkoutPlanBase,
    WorkoutPlanCreate,
    WorkoutPlanRead,
    WorkoutPlanUpdate,
)

__all__ = [
    "AnnouncementBase", "AnnouncementCreate", "AnnouncementRead", "AnnouncementUpdate",
    "AttendanceBase", "AttendanceCreate", "AttendanceRead", "AttendanceUpdate",
    "ExerciseBase", "ExerciseCreate", "ExerciseRead", "ExerciseUpdate",
    "MemberBase", "MemberCreate", "MemberRead", "MemberUpdate",
    "MemberWorkoutBase", "MemberWorkoutCreate", "MemberWorkoutRead", "MemberWorkoutUpdate",
    "MembershipBase", "MembershipCreate", "MembershipRead", "MembershipUpdate",
    "NotificationBase", "NotificationCreate", "NotificationRead", "NotificationUpdate",
    "PaymentBase", "PaymentCreate", "PaymentRead", "PaymentUpdate",
    "ProgressRecordBase", "ProgressRecordCreate", "ProgressRecordRead", "ProgressRecordUpdate",
    "TrainerBase", "TrainerCreate", "TrainerRead", "TrainerUpdate",
    "UserBase", "UserCreate", "UserRead", "UserUpdate",
    "WorkoutExerciseBase", "WorkoutExerciseCreate", "WorkoutExerciseRead", "WorkoutExerciseUpdate",
    "WorkoutLogBase", "WorkoutLogCreate", "WorkoutLogRead", "WorkoutLogUpdate",
    "WorkoutPlanBase", "WorkoutPlanCreate", "WorkoutPlanRead", "WorkoutPlanUpdate",
]