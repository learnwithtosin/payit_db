from sqlalchemy import Column, Integer, String, ForeignKey, Enum, JSON, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base
from .enums import PaymentTypeEnum


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    transaction_id = Column(String(100), nullable=True)  
    payment_gateway = Column(String(100), nullable=False)
    payment_type = Column(Enum(PaymentTypeEnum), nullable=False)
    payload = Column(JSON, nullable=True)  
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)



    # order = relationship("Order", backref="payment")