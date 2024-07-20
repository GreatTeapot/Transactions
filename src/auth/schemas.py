from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, constr, StringConstraints


class UserCreate(BaseModel):
    full_name: Annotated[str, Field(min_length=3, max_length=30)]
    email: EmailStr
    password: Annotated[str, Field(min_length=8, max_length=30)]


class UserRead(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool

    class Config:
        from_attributes = True


class SuperUser(UserCreate):
    is_superuser: bool = True


class UserWithBalance(UserRead):
    balance: float

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    full_name: Annotated[str, Field(min_length=3, max_length=50)]
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str


class TokenRefresh(BaseModel):
    refresh_token: str


class PasswordChange(BaseModel):
    old_password: str
    new_password: str