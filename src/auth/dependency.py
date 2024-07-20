from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from .exceptions import credentials_exception, admin_rights_exception
from .jwt import SECRET_KEY, ALGORITHM
from .models import User
from .schemas import UserRead
from src.utils.unitofwork import UnitOfWork

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_async_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_id = int(user_id)
    except (JWTError, ValueError):
        raise credentials_exception
    user = await session.get(User, user_id)
    if user is None:
        raise credentials_exception
    return UserRead.from_orm(user)


async def get_current_superuser(current_user: UserRead = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise admin_rights_exception
    return current_user


async def get_uow():
    return UnitOfWork()
