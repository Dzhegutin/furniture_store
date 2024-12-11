from fastapi import FastAPI

from app.routes import cart_items


app = FastAPI(title="Cart Service")


# Подключение маршрутов
app.include_router(cart_items.router, prefix="/api/cart", tags=["Cart"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Cart Service!"}
