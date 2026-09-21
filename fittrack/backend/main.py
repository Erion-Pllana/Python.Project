"""
backend/main.py

Run with:
    uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.routers import auth, health

app = FastAPI(
    title=settings.app_name,
    description="FitTrack -- Fitness Center / Gym Management System API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"application": settings.app_name, "status": "running"}