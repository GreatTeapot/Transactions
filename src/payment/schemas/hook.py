from typing import Optional

from pydantic import BaseModel, Field
from pydantic.v1 import validator


class WebhookPayload(BaseModel):
    transaction_id: str
    user_id: Optional[int] = None
    account_id: int
    amount: float
    signature: str = Field(min_length=1)

