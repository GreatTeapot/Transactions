from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.dependency import get_uow, get_current_user, get_current_superuser
from src.auth.schemas import UserRead
from src.payment.schemas.hook import WebhookPayload
from src.payment.services.payment import PaymentService
from src.utils.unitofwork import IUnitOfWork

router = APIRouter(prefix="/payment", tags=["payments"])


@router.post("")
async def process_webhook(data: WebhookPayload,
                          uow: IUnitOfWork = Depends(get_uow),
                          current_user: UserRead = Depends(get_current_user)):
    try:
        await PaymentService().process_webhook(data, uow, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"message": "Transaction processed"}


@router.get("/{user_id}", response_model=List[WebhookPayload])
async def get_user_transactions(user_id: int, current_user: UserRead = Depends(get_current_superuser),
                                uow: IUnitOfWork = Depends(get_uow)):
    transactions = await PaymentService().get_user_transactions(uow, user_id)

    return transactions


@router.get("", response_model=List[WebhookPayload])
async def get_user_transactions(current_user: UserRead = Depends(get_current_user), uow: IUnitOfWork = Depends(get_uow)):
     return await PaymentService().get_user_transactions(uow, current_user.id)
