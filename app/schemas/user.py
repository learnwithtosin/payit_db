import re
from pydantic import BaseModel, constr, EmailStr, validator, constr, Field, field_validator, model_validator
from datetime import datetime
from typing import Optional
from enum import Enum


class GenderEnum(str, Enum):
    male = "M"
    female = "F"


class CategoryEnum(str, Enum):
    buyer = "buyer"
    farmer = "farmer"


class UserCreate(BaseModel):
    name: str = Field(min_length=4, max_length=30)
    phone: str = Field(min_length=11)
    email: EmailStr
    password: str = Field(min_length=6, max_length= 24)
    confirm_password: str
    gender: GenderEnum
    category: CategoryEnum
    location: str = Field(min_length=3)

    @field_validator("password")
    def validate_password(cls, value):
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[^A-Za-z0-9]", value):
            raise ValueError("Password must contain at least one special character.")
        return value

    @model_validator(mode='after')
    def validate_confirm_password(self):
        if self.password != self.confirm_password:
            raise ValueError('passwords must match')
        return self

    @validator("phone")
    def phone_isvalid(cls, value):
        if value.isdigit() is not True:
            raise ValueError("phone number must be digits")
        return value



class UserResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    gender: GenderEnum
    category: CategoryEnum
    location: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserUpdate(BaseModel):
    name: Optional[constr(min_length=4, max_length=20)] = None
    phone: Optional[constr(min_length=11)] = None
    email: Optional[str] = None
    password: Optional[str] = None
    gender: Optional[GenderEnum] = None
    category: Optional[CategoryEnum] = None
    location: Optional[str] = None

    @validator('password')
    def validate_password(cls, v):
        if not (8 <= len(v) <= 15):
            raise ValueError('Password must be between 8 and 15 characters long')
        if not any(c.isalpha() for c in v):
            raise ValueError('Password must contain at least one letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

    class Config:
        from_attributes = True
    
    # class Config:
    #     orm_mode = True
