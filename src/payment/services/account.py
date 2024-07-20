from fastapi import HTTPException
from starlette import status

from src.auth.exceptions import validate_user_existence
from src.auth.schemas import UserWithBalance
from src.utils.unitofwork import IUnitOfWork


class AccountService:
    async def get_user_accounts(self, uow: IUnitOfWork, user_id: int):
        async with uow:
            accounts = await uow.accounts.find_by_user_id(user_id=user_id)
            if not accounts:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="accounts for this user not found")

            return [account.to_read_model() for account in accounts]

    async def get_user_balance(self, uow: IUnitOfWork, user_id: int) -> UserWithBalance:
        async with uow:
            user = await uow.users.find_one(id=user_id)
            validate_user_existence(user)
            accounts = await uow.accounts.find_by_user_id(user_id=user_id)
            balance = sum(account.balance for account in accounts)
            return UserWithBalance(
                    id=user.id,
                    full_name=user.full_name,
                    email=user.email,
                    is_active=user.is_active,
                    is_superuser=user.is_superuser,
                    is_verified=user.is_verified,
                    balance=balance
            )