from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Product
from app.database import get_db
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
router = APIRouter()
from sqlalchemy.future import select
# Создать новый продукт
@router.post("/", response_model=ProductRead)
async def create_product(product: ProductCreate, session: AsyncSession = Depends(get_db)):
    new_product = Product(**product.dict())
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return new_product

# Получить список всех продуктов
@router.get("/", response_model=list[ProductRead])
async def get_products(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Product))
    products = result.scalars().all()
    return products

# Получить продукт по ID
@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, session: AsyncSession = Depends(get_db)):
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Обновить продукт
@router.put("/{product_id}", response_model=ProductRead)
async def update_product(product_id: int, product_update: ProductUpdate, session: AsyncSession = Depends(get_db)):
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product_update.dict().items():
        setattr(product, key, value)
    await session.commit()
    await session.refresh(product)
    return product

# Удалить продукт
@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int, session: AsyncSession = Depends(get_db)):
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await session.delete(product)
    await session.commit()