from pydantic import BaseModel, Field, validator, model_validator
from decimal import Decimal
from enum import Enum as PyEnum
from fastapi import HTTPException

class OrderStatusEnum(str, PyEnum):
    pending = "pending"
    processing = "processing"
    delivered = "delivered"
    cancelled = "cancelled"



class Order(BaseModel):
    product_name: str
    quantity: int = Field(ge=1)


    @validator('quantity')
    def quantity_is_not_zero(cls, value):
        if value < 1:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail = "Quantity can not be zero or less than 1!")
        return value



class OrderRead(Order):
    id: int
    amount: Decimal
    order_status: OrderStatusEnum

    class Config:
        orm_mode = True
