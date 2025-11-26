from pydantic import BaseModel, Field 
from decimal import Decimal
from datetime import datetime
from ..models.enums import CategoryEnum

class ProductCreate(BaseModel):
    name: str = Field(min_length=3)
    unit_price: Decimal
    quantity: int
    category: CategoryEnum

class ProductResponse(ProductCreate):
    created_at: datetime
    updated_at: datetime


    class Config:
        orm_mode = True








# from pydantic import BaseModel, constr, EmailStr, validator, constr
# from datetime import datetime
# from typing import Optional
# from enum import Enum
# from decimal import Decimal




# class CategoryEnum(str, Enum):
#     tubers = "tubers"
#     fruits = "fruits"
#     grains = "grains"
#     vegetables = "vegetables"
#     cereals = "cereals"
#     oils = "oils"
#     livestock = "livestock"
#     latex = "latex"


# class ProductCreate(BaseModel):
#     name: constr(min_length=4, max_length=20)
#     price: Decimal
#     quantity: int
#     category: CategoryEnum



# class ProductResponse(BaseModel):
#     id: int
#     name: constr(min_length=4, max_length=20)
#     price: Decimal
#     quantity: int
#     category: CategoryEnum
#     created_at: Optional[datetime] = None
#     updated_at: Optional[datetime] = None
#     user_id: int


# class ProductUpdate(BaseModel):
#     name: Optional[constr(min_length=4, max_length=20)] = None
#     price: Optional[Decimal] = None
#     quantity: Optional[int] = None
#     category: Optional[CategoryEnum] = None


#     class Config:
#         from_attributes = True
    
#     # class Config:
#     #     orm_mode = True