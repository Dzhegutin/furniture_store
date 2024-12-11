from fastapi import FastAPI
from app.routes import products, categories

app = FastAPI(title="Product Service")

# Подключаем маршруты
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Product Service!"}
