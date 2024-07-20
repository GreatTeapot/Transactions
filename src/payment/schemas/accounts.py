from pydantic import BaseModel


class AccountRead(BaseModel):
    id: int
    user_id: int
    balance: float