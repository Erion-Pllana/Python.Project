"""
backend/models/mixins.py

Shared column sets that multiple models reuse.
"""

from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class TimestampMixin:
    """
    Adds created_at / updated_at to any model that inherits it.
    created_at is set once by the database on insert; updated_at is
    refreshed by the database on every UPDATE.
    """

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )