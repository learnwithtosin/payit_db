from sqlalchemy import Integer, Column, String, DateTime, Enum
from ..schemas.user import GenderEnum, CategoryEnum
from .base import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String(50), min_length=3, max_length=30, nullable=False)
    phone = Column(String(11), unique=True, min_length=11, nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=False)
    gender = Column(Enum(GenderEnum.male.value, GenderEnum.female.value), nullable=False) # create Enum
    category = Column(Enum(CategoryEnum.buyer.value, CategoryEnum.farmer.value), nullable=False) # create ENum
    location = Column(String(255), min_length=3, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # User model
    products = relationship("Product", back_populates="user")

