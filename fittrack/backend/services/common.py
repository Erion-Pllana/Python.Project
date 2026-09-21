"""
backend/services/common.py

Small helpers every resource service reuses.
"""

from contextlib import contextmanager

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


@contextmanager
def commit_or_409(db: Session, message: str = "This operation violates a database constraint."):
    """
    Wrap a db.add()/db.delete() + db.commit() so a SQLAlchemy
    IntegrityError becomes a clean 409 instead of an unhandled 500
    that leaks a raw SQL error message to the client.
    """
    try:
        yield
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=message)


def get_or_404(db: Session, model, object_id: int, name: str):
    """Fetch by primary key or raise a clean 404 naming the resource."""
    obj = db.get(model, object_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{name} not found.")
    return obj