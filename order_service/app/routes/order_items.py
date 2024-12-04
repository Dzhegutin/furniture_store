from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import OrderItem
from app.schemas.order_item import OrderItemRead
from app.database import get_db

router = APIRouter()


@router.get("/{order_id}/items", response_model=List[OrderItemRead])
async def get_order_items(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OrderItem).where(OrderItem.order_id == order_id))
    items = result.scalars().all()
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this order")
    return items
