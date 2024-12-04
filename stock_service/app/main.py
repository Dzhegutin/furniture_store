from fastapi import FastAPI
from app.routes import stocks, stock_items

app = FastAPI(title="Stock Service")

# Подключаем маршруты
app.include_router(stocks.router, prefix="/stocks", tags=["Stocks"])
app.include_router(stock_items.router, prefix="/stock-items", tags=["Stock Items"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Stock Service!"}
