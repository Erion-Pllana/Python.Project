"""
backend/services/member_service.py
"""

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.models.enums import UserRole
from backend.models.member import Member
from backend.models.user import User
from backend.schemas.member import MemberCreate, MemberUpdate
from backend.services.common import commit_or_409, get_or_404


def list_members(db: Session, skip: int = 0, limit: int = 50, search: Optional[str] = None) -> list[Member]:
    query = db.query(Member)
    if search:
        like = f"%{search}%"
        query = query.filter(or_(Member.first_name.ilike(like), Member.last_name.ilike(like)))
    return query.order_by(Member.id).offset(skip).limit(limit).all()


def get_member(db: Session, member_id: int) -> Member:
    return get_or_404(db, Member, member_id, "Member")


def get_member_by_user_id(db: Session, user_id: int) -> Optional[Member]:
    return db.query(Member).filter(Member.user_id == user_id).first()


def create_member(db: Session, payload: MemberCreate) -> Member:
    """
    Creates a Member profile for an *existing* user account (the user
    must already exist with role MEMBER and have no profile yet --
    this is for an admin attaching/repairing a profile, not normal
    sign-up, which goes through POST /api/auth/register).
    """
    user = db.get(User, payload.user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    if user.role != UserRole.MEMBER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only a user with role MEMBER can have a member profile.",
        )
    if get_member_by_user_id(db, payload.user_id) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This user already has a member profile.",
        )

    member = Member(**payload.model_dump())
    db.add(member)
    with commit_or_409(db, "Could not create member."):
        pass
    db.refresh(member)
    return member


def update_member(db: Session, member_id: int, payload: MemberUpdate) -> Member:
    member = get_member(db, member_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(member, field, value)
    with commit_or_409(db, "Could not update member."):
        pass
    db.refresh(member)
    return member


def delete_member(db: Session, member_id: int) -> None:
    member = get_member(db, member_id)
    db.delete(member)
    with commit_or_409(db, "Could not delete member -- they may still have related records."):
        pass