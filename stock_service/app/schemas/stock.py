from pydantic import BaseModel
from typing import Optional


class StockBase(BaseModel):
    location: str
    capacity: int

# Схема для вывода данных о складе с полем id
class StockOut(StockBase):
    id: int

    class Config:
        orm_mode = True

class StockCreate(StockBase):
    pass


class StockUpdate(BaseModel):
    location: Optional[str]
    capacity: Optional[int]


class StockResponse(StockBase):
    id: int

    class Config:
        orm_mode = True
