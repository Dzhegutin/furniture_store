import httpx
from fastapi import HTTPException
from fastapi.params import Header
from starlette import status

USER_SERVICE_URL = "http://user_service:8000/api"
PRODUCT_SERVICE_URL = "http://product_service:8001/api"
ORDER_SERVICE_URL = "http://order_service:8002/api"
STOCK_SERVICE_URL = "http://stock_service:8004/api"


async def get_current_user(token: str = Header(...)):
    if not token.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token format"
        )

    token_value = token[len("Bearer "):]
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{USER_SERVICE_URL}/auth/jwt/verify-token",
            headers={"Authorization": f"Bearer {token_value}"}
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token"
        )

    # Вернуть информацию о пользователе, если токен валиден
    return response.json()


async def get_product_from_service(product_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Product not found")
        return response.json()


async def get_stock_from_service(product_id: int, stock_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{STOCK_SERVICE_URL}/?product_id={product_id}&stock_id={stock_id}"
        )
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Stock not found")
        return response.json()


async def create_order_in_order_service(cart, user, order_data):
    payload = {
        "user_id": user["id"],
        "items": [
            {
                "product_id": item.product_id,
                "warehouse_id": item.warehouse_id,
                "quantity": item.quantity,
                "price": item.price,
            }
            for item in cart.cart_items
        ],
        "delivery_address": order_data.delivery_address,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(ORDER_SERVICE_URL, json=payload)
        if response.status_code != 201:
            raise HTTPException(status_code=400, detail="Failed to create order")
        return response.json()
