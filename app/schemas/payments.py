from pydantic import BaseModel
from enum import Enum as PyEnum
from typing import Optional, Dict

class PaymentTypeEnum(str, PyEnum):
    card = "card"
    transfer = "transfer"
    wallet = "wallet"

class PaymentBase(BaseModel):
    order_id: int
    payment_gateway: str
    payment_type: PaymentTypeEnum
    payload: Optional[Dict] = None

class PaymentCreate(PaymentBase):
    transaction_id: Optional[str] = None

class PaymentRead(PaymentBase):
    id: int
    transaction_id: Optional[str] = None

    class Config:
        orm_mode = True
