from src.payment.models.payments import Payment
from src.utils.repository import SQLAlchemyRepository


class TransactionsRepository(SQLAlchemyRepository):
    model = Payment