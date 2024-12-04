from pydantic import BaseModel

# Базовая схема для создания продукта
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
    category_id: int

# Базовая схема для чтения продукта
class ProductRead(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int
    category_id: int

    class Config:
        orm_mode = True

# Базовая схема для обновления продукта
class ProductUpdate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
