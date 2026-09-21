"""
backend/routers/health.py

Simple health-check endpoint used by the Streamlit frontend (and by
humans / monitoring tools) to confirm the FastAPI backend is running.
"""

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/api/health")
def health_check():
    """Return a basic status payload confirming the API is alive."""
    return {
        "status": "ok",
        "application": "FitTrack",
    }