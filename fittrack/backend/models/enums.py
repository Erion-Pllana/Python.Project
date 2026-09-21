"""
backend/models/enums.py

All the fixed vocabularies used across FitTrack's tables, in one place
so a status/role/type name is spelled the same way everywhere. Each is
a str-Enum so it serializes cleanly to/from JSON in FastAPI and maps to
a native MySQL ENUM column via SQLAlchemy.
"""

import enum


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    TRAINER = "TRAINER"
    MEMBER = "MEMBER"


class Gender(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
    PREFER_NOT_TO_SAY = "PREFER_NOT_TO_SAY"


class MembershipType(str, enum.Enum):
    BASIC = "BASIC"
    STANDARD = "STANDARD"
    PREMIUM = "PREMIUM"
    VIP = "VIP"


class MembershipStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"
    PENDING = "PENDING"


class DifficultyLevel(str, enum.Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"


class ExerciseCategory(str, enum.Enum):
    CARDIO = "CARDIO"
    STRENGTH = "STRENGTH"
    FLEXIBILITY = "FLEXIBILITY"
    BALANCE = "BALANCE"
    HIIT = "HIIT"
    SPORTS = "SPORTS"
    OTHER = "OTHER"


class MemberWorkoutStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    PAUSED = "PAUSED"
    CANCELLED = "CANCELLED"


class PaymentMethod(str, enum.Enum):
    CASH = "CASH"
    CARD = "CARD"
    BANK_TRANSFER = "BANK_TRANSFER"
    ONLINE = "ONLINE"


class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class AnnouncementAudience(str, enum.Enum):
    ALL = "ALL"
    MEMBER = "MEMBER"
    TRAINER = "TRAINER"


class NotificationType(str, enum.Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    SUCCESS = "SUCCESS"
    PAYMENT = "PAYMENT"
    WORKOUT = "WORKOUT"
    ANNOUNCEMENT = "ANNOUNCEMENT"
    ATTENDANCE = "ATTENDANCE"