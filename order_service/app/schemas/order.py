from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.schemas.order_item import OrderItemCreate, OrderItemRead


class OrderBase(BaseModel):
    customer_id: int
    status: str
    total_price: float


class OrderCreate(OrderBase):
    order_items: List[OrderItemCreate]


class OrderRead(OrderBase):
    id: int
    order_date: datetime
    order_items: List[OrderItemRead]

    class Config:
        orm_mode = True
