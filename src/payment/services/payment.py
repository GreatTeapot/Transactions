# service.py
import hashlib
from fastapi import HTTPException
from src.payment.schemas.hook import WebhookPayload
from src.utils.unitofwork import IUnitOfWork
from src.config import SECRET_KEY


class PaymentService:
    @staticmethod
    def hash_signature(payload: WebhookPayload):
        data = f"{payload.account_id}{payload.amount}{payload.transaction_id}{payload.user_id}{SECRET_KEY}"
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def verify_signature(payload: WebhookPayload):
        expected_signature = PaymentService.hash_signature(payload)
        if expected_signature != payload.signature:
            raise HTTPException(status_code=400, detail="Invalid signature")

    async def process_webhook(self, payload: WebhookPayload, uow: IUnitOfWork, user_id: int):
        async with uow:
            payload.user_id = user_id
            payload.signature = self.hash_signature(payload)
            self.verify_signature(payload)

            transaction = await uow.transactions.find_one(transaction_id=payload.transaction_id)
            if transaction:
                raise HTTPException(status_code=400, detail="Transaction already processed")

            account = await uow.accounts.find_one(user_id=payload.user_id, id=payload.account_id)
            if not account:
                account = await uow.accounts.add_one(
                    {"user_id": payload.user_id, "id": payload.account_id, "balance": 0})
            if account.id != payload.account_id:
                payload.account_id = account.id

            await uow.transactions.add_one({
                "transaction_id": payload.transaction_id,
                "user_id": payload.user_id,
                "account_id": payload.account_id,
                "amount": payload.amount,
                "signature": payload.signature
            })

            await uow.accounts.edit_one(account.id, {"balance": account.balance + payload.amount})
            await uow.commit()

    async def get_user_transactions(self, uow: IUnitOfWork, user_id: int):
        async with uow:
            transactions = await uow.transactions.find_by_user_id(user_id=user_id)
            if not transactions:
                raise HTTPException(status_code=404, detail="No transactions found for this user")

            return [transaction.to_read_model() for transaction in transactions]