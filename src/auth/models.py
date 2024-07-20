from datetime import datetime, timedelta
from typing import Optional
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from sqlalchemy import (JSON, TIMESTAMP, Boolean, Column, ForeignKey, Integer,
                        String, Table)

from src.auth.schemas import UserRead
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(SQLAlchemyBaseUserTable[int],Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String ,nullable=False)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    accounts = relationship("Account", back_populates="user")
    payments = relationship("Payment", back_populates="user")

    def to_read_model(self) -> UserRead:
        return UserRead(
            id=self.id,
            full_name=self.full_name,
            email=self.email,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            is_verified=self.is_verified,
        )