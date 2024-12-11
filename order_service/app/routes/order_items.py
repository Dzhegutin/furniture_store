from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import OrderItem, Order
from app.schemas.order_item import OrderItemRead
from app.database import get_db

router = APIRouter()


@router.get("/{order_id}/items", response_model=List[OrderItemRead])
async def get_order_items(order_id: int, db: AsyncSession = Depends(get_db)):
    # Загрузка заказа с элементами заказа с использованием selectinload для оптимизации запросов
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.order_items))  # Оптимизация с помощью selectinload
        .where(Order.id == order_id)
    )
    order = result.scalars().first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Возвращаем только элементы заказа
    if not order.order_items:
        raise HTTPException(status_code=404, detail="No items found for this order")

    return order.order_items
