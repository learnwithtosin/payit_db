from sqlalchemy import Integer, Column, String, DateTime, Enum, DECIMAL, ForeignKey
# from sqlalchemy.orm import DeclarativeBase
from .base import Base
from sqlalchemy.sql import func
# from .user_model import User
from sqlalchemy.orm import relationship



class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String(50), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    category = Column(Enum('grains', 'tubers', 'vegetables', 'fruits', 'livestock', 'cereals', 'oils', 'latex'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="products")

