"""
backend/models/payment.py
"""

from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship

from backend.database.session import Base
from backend.models.enums import PaymentMethod, PaymentStatus
from backend.models.mixins import TimestampMixin


class Payment(Base, TimestampMixin):
    """
    A payment made by a member. Usually for a specific membership
    (membership_id set), but that link is optional so one-off charges
    (a class drop-in, a fee) are also possible.
    """

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(
        Integer, ForeignKey("members.id", ondelete="CASCADE"), nullable=False, index=True
    )
    membership_id = Column(
        Integer, ForeignKey("memberships.id", ondelete="SET NULL"), nullable=True, index=True
    )

    amount = Column(Numeric(8, 2), nullable=False)
    payment_date = Column(Date, nullable=False)
    payment_method = Column(SAEnum(PaymentMethod, name="payment_method"), nullable=False)
    status = Column(
        SAEnum(PaymentStatus, name="payment_status"),
        nullable=False,
        default=PaymentStatus.PENDING,
    )
    transaction_reference = Column(String(100), unique=True, nullable=True)

    member = relationship("Member", back_populates="payments")
    membership = relationship("Membership", back_populates="payments")

    def __repr__(self) -> str:
        return f"<Payment id={self.id} member={self.member_id} amount={self.amount} status={self.status}>"