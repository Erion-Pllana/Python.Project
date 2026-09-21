"""
backend/models/membership.py
"""

from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship

from backend.database.session import Base
from backend.models.enums import MembershipStatus, MembershipType
from backend.models.mixins import TimestampMixin


class Membership(Base, TimestampMixin):
    """
    One row per membership period a member has purchased -- the
    initial sign-up, each renewal, an upgrade, etc. A member's full
    membership history is just their rows here, ordered by start_date;
    the current one is whichever row has status ACTIVE.
    """

    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(
        Integer, ForeignKey("members.id", ondelete="CASCADE"), nullable=False, index=True
    )

    membership_type = Column(SAEnum(MembershipType, name="membership_type"), nullable=False)
    status = Column(
        SAEnum(MembershipStatus, name="membership_status"),
        nullable=False,
        default=MembershipStatus.PENDING,
    )
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    fee = Column(Numeric(8, 2), nullable=False)

    member = relationship("Member", back_populates="memberships")
    payments = relationship("Payment", back_populates="membership")

    def __repr__(self) -> str:
        return f"<Membership id={self.id} member_id={self.member_id} type={self.membership_type}>"