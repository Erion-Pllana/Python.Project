"""
backend/database/seed_demo_users.py

Creates the three development demo accounts if they don't already
exist. Safe to re-run -- checks by email first, never duplicates.

Run with:
    python -m backend.database.seed_demo_users
"""

from datetime import date

from backend.database.session import SessionLocal
from backend.models.enums import UserRole
from backend.models.member import Member
from backend.models.trainer import Trainer
from backend.models.user import User
from backend.security.security import hash_password

import backend.models  # noqa: F401

DEMO_PASSWORD = "FitTrack#2026"

DEMO_ACCOUNTS = [
    {"username": "admin", "email": "admin@fittrack.local", "role": UserRole.ADMIN},
    {"username": "trainer", "email": "trainer@fittrack.local", "role": UserRole.TRAINER},
    {"username": "member", "email": "member@fittrack.local", "role": UserRole.MEMBER},
]


def seed_demo_users() -> None:
    db = SessionLocal()
    try:
        for account in DEMO_ACCOUNTS:
            existing = db.query(User).filter(User.email == account["email"]).first()
            if existing is not None:
                continue

            user = User(
                username=account["username"],
                email=account["email"],
                password_hash=hash_password(DEMO_PASSWORD),
                role=account["role"],
                is_active=True,
            )
            db.add(user)
            db.flush()

            if account["role"] == UserRole.TRAINER:
                db.add(Trainer(
                    user_id=user.id, first_name="Demo", last_name="Trainer",
                    specialization="General Fitness", hire_date=date.today(),
                ))
            elif account["role"] == UserRole.MEMBER:
                db.add(Member(
                    user_id=user.id, first_name="Demo", last_name="Member",
                    join_date=date.today(),
                ))

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_users()
    print("Demo accounts ready:")
    for account in DEMO_ACCOUNTS:
        print(f"  {account['role'].value:<8} {account['email']}  (password: {DEMO_PASSWORD})")