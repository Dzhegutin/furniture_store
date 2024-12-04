from fastapi import FastAPI
from app.routes import orders, order_items

app = FastAPI(title="Order Service")

# Подключение маршрутов
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(order_items.router, prefix="/order_items", tags=["Order Items"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Order Service!"}
