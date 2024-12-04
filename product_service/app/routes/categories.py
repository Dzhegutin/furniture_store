from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Category
from app.database import get_db
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
router = APIRouter()

# Создать новую категорию
@router.post("/", response_model=CategoryRead)
async def create_category(category: CategoryCreate, session: AsyncSession = Depends(get_db)):
    new_category = Category(**category.dict())
    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)
    return new_category

# Получить список всех категорий
@router.get("/", response_model=list[CategoryRead])
async def get_categories(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Category))
    categories = result.scalars().all()
    return categories

# Получить категорию по ID
@router.get("/{category_id}", response_model=CategoryRead)
async def get_category(category_id: int, session: AsyncSession = Depends(get_db)):
    category = await session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# Обновить категорию
@router.put("/{category_id}", response_model=CategoryRead)
async def update_category(category_id: int, category_update: CategoryUpdate, session: AsyncSession = Depends(get_db)):
    category = await session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in category_update.dict().items():
        setattr(category, key, value)
    await session.commit()
    await session.refresh(category)
    return category

# Удалить категорию
@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: int, session: AsyncSession = Depends(get_db)):
    category = await session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    await session.delete(category)
    await session.commit()
