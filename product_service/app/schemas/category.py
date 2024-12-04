from pydantic import BaseModel

# Схема для создания категории
class CategoryCreate(BaseModel):
    name: str

# Схема для чтения категории
class CategoryRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# Схема для обновления категории
class CategoryUpdate(BaseModel):
    name: str
