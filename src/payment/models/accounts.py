from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.payment.schemas.accounts import AccountRead


class Account(Base):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    balance: Mapped[float] = mapped_column(Float, nullable=False, )

    user = relationship("User", back_populates="accounts")
    payments = relationship("Payment", back_populates="accounts")

    def to_read_model(self) -> AccountRead:
        return AccountRead(
            id=self.user_id,
            user_id=self.user_id,
            balance=self.balance,
        )