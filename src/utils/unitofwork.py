from abc import ABC, abstractmethod
from typing import Type

from src.database import async_session_maker
from src.auth.repository import UsersRepository
from src.payment.repository.accounts import AccountsRepository
from src.payment.repository.payment import TransactionsRepository


# https://github1s.com/cosmicpython/code/tree/chapter_06_uow
class IUnitOfWork(ABC):
    users: Type[UsersRepository]
    transactions: Type[TransactionsRepository]
    accounts: Type[AccountsRepository]

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = UsersRepository(self.session)
        self.transactions = TransactionsRepository(self.session)
        self.accounts = AccountsRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
