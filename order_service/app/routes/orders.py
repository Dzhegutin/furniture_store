from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import Order, OrderItem
from app.schemas.order import OrderCreate, OrderRead
from app.database import get_db

router = APIRouter()


@router.post("/", response_model=OrderRead)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    try:
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

        stmt = select(Order).options(
            selectinload(Order.order_items)
        ).where(Order.id == new_order.id)

        result = await db.execute(stmt)
        order_with_items = result.scalar_one()

        return order_with_items

    except SQLAlchemyError as e:
        await db.rollback()
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    # Получаем заказ с элементами с помощью selectinload для оптимизации
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.order_items))  # Загружаем элементы заказа
        .where(Order.id == order_id)
    )
    order = result.scalars().first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


@router.get("/", response_model=List[OrderRead])
async def get_orders(db: AsyncSession = Depends(get_db)):
    # Получаем все заказы, добавляем selectinload для загрузки элементов заказа
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.order_items))  # Загружаем элементы для каждого заказа
    )
    orders = result.scalars().all()
    return orders
