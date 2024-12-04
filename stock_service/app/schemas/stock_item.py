from pydantic import BaseModel
from typing import Optional


class StockItemBase(BaseModel):
    stock_id: int
    product_id: int
    quantity: int


class StockItemCreate(StockItemBase):
    pass


class StockItemUpdate(BaseModel):
    quantity: int


class StockItemResponse(StockItemBase):
    id: int

    class Config:
        orm_mode = True
