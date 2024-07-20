from fastapi import APIRouter, Depends
from typing import List
from src.auth.dependency import get_current_user, get_uow, get_current_superuser
from src.auth.schemas import UserRead
from src.payment.schemas.accounts import AccountRead
from src.payment.services.account import AccountService
from src.utils.unitofwork import IUnitOfWork

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("", response_model=List[AccountRead])
async def get_accounts(current_user: UserRead = Depends(get_current_user),
                       uow: IUnitOfWork = Depends(get_uow)):

    accounts = await AccountService().get_user_accounts(uow, current_user.id)
    return accounts


@router.get("/{user_id}", response_model=List[AccountRead])
async def get_user_accounts(user_id: int, current_user: UserRead = Depends(get_current_superuser), uow: IUnitOfWork = Depends(get_uow)):

    accounts = await AccountService().get_user_accounts(uow, user_id)
    return accounts