from enum import Enum

class GenderEnum(str, Enum):
    male = "MALE"
    female = "FEMALE"

class CategoryEnum(str, Enum):
    tubers = "tubers"
    fruits = "fruits"
    grains = "grains"
    vegetables = "vegetables"
    cereals = "cereals"
    oils = "oils"
    livestock = "livestock"
    latex = "latex"

class OrderStatusEnum(str, Enum):
    pending = "pending"
    processing = "processing"
    delivered = "delivered"
    cancelled = "cancelled"


class PaymentTypeEnum(str, Enum):
    card = "card"
    transfer = "transfer"
    wallet = "wallet"