from pydantic import BaseModel

class TransactionBase(BaseModel):
    order_id: int
    payment_id: int

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id: int

    class Config:
        orm_mode = True
