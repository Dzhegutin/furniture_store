from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Stock
from app.database import get_db
from app.schemas.stock import StockCreate, StockUpdate, StockResponse, StockOut

router = APIRouter()

@router.post("/", response_model=StockResponse)
async def create_stock(stock: StockCreate, db: AsyncSession = Depends(get_db)):
    new_stock = Stock(location=stock.location, capacity=stock.capacity)
    db.add(new_stock)
    await db.commit()
    await db.refresh(new_stock)
    return new_stock

@router.get("/", response_model=list[StockOut])
async def get_all_stocks(db: AsyncSession = Depends(get_db)):
    # Выполняем запрос к базе данных для получения всех складов
    result = await db.execute(select(Stock))
    stocks = result.scalars().all()
    return stocks

@router.get("/{stock_id}", response_model=StockResponse)
async def get_stock(stock_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Stock).where(Stock.id == stock_id))
    stock = result.scalars().first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock


@router.put("/{stock_id}", response_model=StockResponse)
async def update_stock(stock_id: int, stock: StockUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Stock).where(Stock.id == stock_id))
    db_stock = result.scalars().first()
    if not db_stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    if stock.location is not None:
        db_stock.location = stock.location
    if stock.capacity is not None:
        db_stock.capacity = stock.capacity

    await db.commit()
    await db.refresh(db_stock)
    return db_stock


@router.delete("/{stock_id}")
async def delete_stock(stock_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Stock).where(Stock.id == stock_id))
    stock = result.scalars().first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    await db.delete(stock)
    await db.commit()
    return {"detail": "Stock deleted successfully"}
