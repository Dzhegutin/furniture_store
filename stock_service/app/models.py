from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String(255), nullable=False)
    capacity = Column(Integer, nullable=False)

    # Связь с позициями на складе
    stock_items = relationship('StockItem', back_populates='stock')


class StockItem(Base):
    __tablename__ = 'stock_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_id = Column(Integer, ForeignKey('stocks.id'), nullable=False)
    product_id = Column(Integer, nullable=False)  # Ссылка на `products.id` из другого микросервиса
    quantity = Column(Integer, nullable=False)

    # Связь со складом
    stock = relationship('Stock', back_populates='stock_items')
