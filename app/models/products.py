from sqlalchemy import Integer, Column, String, DateTime, Enum, DECIMAL, ForeignKey
from .base import Base
from sqlalchemy.sql import func
# from .user_model import User
from sqlalchemy.orm import relationship



class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    farmer_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    image_url = Column(String(255), nullable= True)
    name = Column(String(50), nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


    # farmer = relationship("Farmer", back_populates="farmer_products")
    # category = relationship("Category", back_populates="products")

# from sqlalchemy import Integer, Column, String, DateTime, Enum, func, Text, ForeignKey
# from sqlalchemy import Enum as SQLEnum
# from sqlalchemy.orm import relationship
# from .base import Base
# from ..enums import ProductCategory, ProductStatus, ProuductUint

# class Product(Base):

#     __tablename__ = "products"

#     id = Column(Integer, primary_key=True, nullable=False, index = True)
#     name = Column(String(30), min_length=3, max_length=30, nullable=False)
#     farmer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable= False, index= True)
#     description = Column(Text, nullable=False)
#     category = Column(SQLEnum(ProductCategory), nullable= False)
#     status = Column(SQLEnum(ProductStatus, default = ProductStatus.available, nullable = False))
#     unit = Column(SQLEnum(ProuductUint), nullable= False)
#     location = Column(String(255), nullable= False)
#     image_url = Column(String(255), nullable= False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
#     updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # farmer = relationship("User" , back_populates="products")