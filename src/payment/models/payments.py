from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.payment.schemas.hook import WebhookPayload


class Payment(Base):
    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    transaction_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey('accounts.id'), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    signature: Mapped[str] = mapped_column(String, nullable=False)

    user = relationship("User", back_populates="payments")
    accounts = relationship("Account", back_populates="payments")

    def to_read_model(self) -> WebhookPayload:
        return WebhookPayload(
            transaction_id=self.transaction_id,
            user_id=self.user_id,
            account_id=self.account_id,
            amount=self.amount,
            signature=self.signature,
        )