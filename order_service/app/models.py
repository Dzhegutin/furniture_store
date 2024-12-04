from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, nullable=False)  # Ссылка на `users.id` из другого микросервиса
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), nullable=False)
    total_price = Column(Float, nullable=False)

    # Связь с позициями заказа
    order_items = relationship('OrderItem', back_populates='order')


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)  # Внешний ключ внутри микросервиса
    product_id = Column(Integer, nullable=False)  # Ссылка на `products.id` из другого микросервиса
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    # Связь с заказом
    order = relationship('Order', back_populates='order_items')
