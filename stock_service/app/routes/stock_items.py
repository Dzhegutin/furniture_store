from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import StockItem
from app.database import get_db
from app.schemas.stock_item import StockItemCreate, StockItemUpdate, StockItemResponse

router = APIRouter()

@router.post("/", response_model=StockItemResponse)
async def create_stock_item(stock_item: StockItemCreate, db: AsyncSession = Depends(get_db)):
    new_stock_item = StockItem(
        stock_id=stock_item.stock_id,
        product_id=stock_item.product_id,
        quantity=stock_item.quantity
    )
    db.add(new_stock_item)
    await db.commit()
    await db.refresh(new_stock_item)
    return new_stock_item


@router.get("/{stock_item_id}", response_model=StockItemResponse)
async def get_stock_item(stock_item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StockItem).where(StockItem.id == stock_item_id))
    stock_item = result.scalars().first()
    if not stock_item:
        raise HTTPException(status_code=404, detail="StockItem not found")
    return stock_item


@router.put("/{stock_item_id}", response_model=StockItemResponse)
async def update_stock_item(stock_item_id: int, stock_item: StockItemUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StockItem).where(StockItem.id == stock_item_id))
    db_stock_item = result.scalars().first()
    if not db_stock_item:
        raise HTTPException(status_code=404, detail="StockItem not found")

    db_stock_item.quantity = stock_item.quantity
    await db.commit()
    await db.refresh(db_stock_item)
    return db_stock_item


@router.delete("/{stock_item_id}")
async def delete_stock_item(stock_item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StockItem).where(StockItem.id == stock_item_id))
    stock_item = result.scalars().first()
    if not stock_item:
        raise HTTPException(status_code=404, detail="StockItem not found")

    await db.delete(stock_item)
    await db.commit()
    return {"detail": "StockItem deleted successfully"}
