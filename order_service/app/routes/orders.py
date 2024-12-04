from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Order, OrderItem
from app.schemas.order import OrderCreate, OrderRead
from app.database import get_db

router = APIRouter()


@router.post("/", response_model=OrderRead)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    new_order = Order(
        customer_id=order.customer_id,
        status=order.status,
        total_price=order.total_price
    )
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)

    for item in order.order_items:
        db.add(OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        ))
    await db.commit()
    await db.refresh(new_order)
    return new_order


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/", response_model=List[OrderRead])
async def get_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order))
    return result.scalars().all()
