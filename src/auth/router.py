from typing import List

from fastapi import APIRouter, Depends

from .schemas import UserCreate, UserUpdate, UserLogin, PasswordChange, TokenRefresh, UserWithBalance, SuperUser
from .service import UserService
from .dependency import get_uow, get_current_user, get_current_superuser
from .schemas import UserRead
from src.utils.unitofwork import IUnitOfWork
from ..payment.services.account import AccountService

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", status_code=201)
async def register(user: UserCreate, uow: IUnitOfWork = Depends(get_uow)):
    result = await UserService().create_user(uow, user)
    return result


@router.post("/superuser", status_code=201)
async def create_superuser(user: SuperUser, uow: IUnitOfWork = Depends(get_uow)):

    result = await UserService().create_superuser(uow, user)
    return result


@router.post("/login")
async def login(user: UserLogin, uow: IUnitOfWork = Depends(get_uow)):
    result = await UserService().authenticate_user(uow, user.email, user.password)
    return result


@router.get("/profile", response_model=UserRead)
async def get_profile(current_user: UserRead = Depends(get_current_user), uow: IUnitOfWork = Depends(get_uow)):
    user = await UserService().get_user(uow, current_user.id)
    return user


@router.put("/profile", response_model=UserRead)
@router.patch("/profile", response_model=UserRead)
async def update_profile(user: UserUpdate, current_user: UserRead = Depends(get_current_user), uow: IUnitOfWork = Depends(get_uow)):
    await UserService().update_user(uow, current_user.id, user)
    updated_user = await UserService().get_user(uow, current_user.id)
    return updated_user



@router.post("/refresh")
async def refresh_access_token(token: TokenRefresh, uow: IUnitOfWork = Depends(get_uow)):
    access_token = await UserService().refresh_access_token(token.refresh_token)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(token: TokenRefresh, uow: IUnitOfWork = Depends(get_uow)):
    await UserService().logout(token.refresh_token)
    return {"message": "Logged out"}


@router.post("/change_password")
async def change_password(password_data: PasswordChange, current_user: UserRead = Depends(get_current_user), uow: IUnitOfWork = Depends(get_uow)):
    await UserService().change_password(uow, current_user.id, password_data)
    return {"message": "Password changed"}


# @router.get("/{user_id}", response_model=UserRead)
# async def get_user(user_id: int, uow: IUnitOfWork = Depends(get_uow)):
#     user = await UserService().get_user(uow, user_id)
#
#     return user


@router.get("/{user_id}", response_model=UserWithBalance)
async def get_user(user_id: int,
                   uow: IUnitOfWork = Depends(get_uow),
                   current_user: UserRead = Depends(get_current_superuser)):

        user = await AccountService().get_user_balance(uow, user_id)
        return user



@router.put("/{user_id}", response_model=UserRead)
@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user: UserUpdate, current_user: UserRead = Depends(get_current_superuser),
                      uow: IUnitOfWork = Depends(get_uow)):
    await UserService().update_user(uow, user_id, user)
    updated_user = await UserService().get_user(uow, user_id)
    return updated_user


@router.delete("/{user_id}")
async def delete_user(user_id: int, current_user: UserRead = Depends(get_current_superuser),
                      uow: IUnitOfWork = Depends(get_uow)):
    await UserService().delete_user(uow, user_id)
    return {"msg": "User deleted"}


@router.get("/users/all", response_model=List[UserRead])
async def get_all_users(uow: IUnitOfWork = Depends(get_uow),
                    ):
    users = await UserService().get_all_users(uow)
    return users