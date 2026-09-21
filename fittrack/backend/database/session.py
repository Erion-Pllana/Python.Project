"""
backend/database/session.py

SQLAlchemy engine and session setup for MySQL.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from backend.config import settings

# The engine is created lazily by SQLAlchemy (no connection is opened
# until something actually queries the database), so importing this
# module is safe even if MySQL isn't running yet.
engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)

# Base class that all future SQLAlchemy models (backend/models/*) will
# inherit from.
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that yields a database session and guarantees
    it is closed afterward. Not used by any route yet in Step 1/2.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()