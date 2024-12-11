from pydantic import BaseModel
from typing import List, Optional


# Схема для добавления товара в корзину
class CartItemCreate(BaseModel):
    product_id: int
    stock_id: int
    quantity: int


# Схема для информации о товаре в корзине
class CartItemResponse(BaseModel):
    product_id: int
    stock_id: int
    quantity: int
    price: float


# Схема для отображения корзины
class CartResponse(BaseModel):
    cart_items: List[CartItemResponse]


# Схема для оформления заказа
class OrderCreate(BaseModel):
    address: str
    payment_method: str
