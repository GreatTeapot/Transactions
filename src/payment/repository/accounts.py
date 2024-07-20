from src.payment.models.accounts import Account
from src.utils.repository import SQLAlchemyRepository


class AccountsRepository(SQLAlchemyRepository):
    model = Account