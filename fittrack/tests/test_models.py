"""
tests/test_models.py

Confirms the SQLAlchemy model layer itself is correct: every model
imports cleanly, registers on Base.metadata, and the full schema (all
14 tables, every foreign key) can actually be created.

This runs against a throwaway in-memory SQLite database rather than
MySQL, so it needs no running database server -- it's a fast sanity
check for the models, not a substitute for running
`python -m backend.database.init_db` against real MySQL.

Run with:
    pytest tests/test_models.py -v
"""

from sqlalchemy import create_engine, inspect

from backend.database.session import Base
import backend.models  # noqa: F401  (registers every model on Base.metadata)

EXPECTED_TABLES = {
    "users",
    "members",
    "trainers",
    "memberships",
    "exercises",
    "workout_plans",
    "workout_exercises",
    "member_workouts",
    "workout_logs",
    "attendance",
    "payments",
    "announcements",
    "notifications",
    "progress_records",
}


def test_all_models_registered_on_metadata():
    table_names = set(Base.metadata.tables.keys())
    assert EXPECTED_TABLES.issubset(table_names), (
        f"Missing tables: {EXPECTED_TABLES - table_names}"
    )


def test_schema_creates_successfully_in_sqlite():
    """
    If every relationship/ForeignKey is wired correctly, this succeeds
    against any SQL backend -- SQLite here, MySQL for the real app.
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    created_tables = set(inspector.get_table_names())

    assert EXPECTED_TABLES.issubset(created_tables)


def test_users_table_has_expected_columns():
    users_table = Base.metadata.tables["users"]
    column_names = {c.name for c in users_table.columns}
    assert {"id", "username", "email", "password_hash", "role", "is_active",
            "created_at", "updated_at"}.issubset(column_names)


def test_foreign_keys_point_at_correct_tables():
    members_table = Base.metadata.tables["members"]
    fk_targets = {fk.column.table.name for fk in members_table.foreign_keys}
    assert fk_targets == {"users"}

    workout_exercises_table = Base.metadata.tables["workout_exercises"]
    fk_targets = {fk.column.table.name for fk in workout_exercises_table.foreign_keys}
    assert fk_targets == {"workout_plans", "exercises"}