from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.models import Cart, CartItem
from app.database import get_db
from app.schemas.cart_item import CartItemCreate, CartResponse, OrderCreate
from app.services import (
    get_current_user,
    get_product_from_service,
    get_stock_from_service,
    create_order_in_order_service,
)

router = APIRouter()



@router.post("/cart/items/")
async def add_to_cart(
        item: CartItemCreate,
        db: Session = Depends(get_db),
        user: dict = Depends(get_current_user),  # Проверка авторизации
):
    product = await get_product_from_service(item.product_id)

    return {"product": product, "user": user}
    # stock = await get_stock_from_service(item.product_id, item.stock_id)
    #
    # if not product or stock["quantity"] < item.quantity:
    #     raise HTTPException(status_code=400, detail="Product not available")
    #
    # cart = db.query(Cart).filter(Cart.user_id == user["id"]).first()
    # if not cart:
    #     cart = Cart(user_id=user["id"])
    #     db.add(cart)
    #     db.commit()
    #
    # cart_item = CartItem(
    #     cart_id=cart.id,
    #     product_id=item.product_id,
    #     warehouse_id=item.warehouse_id,
    #     quantity=item.quantity,
    #     price=product["price"],
    # )
    # db.add(cart_item)
    # db.commit()
    # return {"message": "Item added to cart"}


# @router.get("/cart/", response_model=CartResponse)
# async def get_cart(
#         db: Session = Depends(get_db),
#         token: str = Header(...),
# ):
#     user = await get_user_from_service(token)
#     cart = db.query(Cart).filter(Cart.user_id == user["id"]).first()
#     if not cart:
#         return {"cart_items": []}
#
#     return {
#         "cart_items": [
#             {
#                 "product_id": item.product_id,
#                 "warehouse_id": item.warehouse_id,
#                 "quantity": item.quantity,
#                 "price": item.price,
#             }
#             for item in cart.cart_items
#         ]
#     }
#
#
# @router.delete("/cart/items/{item_id}/")
# async def remove_from_cart(
#         item_id: int,
#         db: Session = Depends(get_db),
#         token: str = Header(...),
# ):
#     user = await get_user_from_service(token)
#     cart_item = db.query(CartItem).filter(CartItem.id == item_id).first()
#     if not cart_item or cart_item.cart.user_id != user["id"]:
#         raise HTTPException(status_code=404, detail="Item not found")
#
#     db.delete(cart_item)
#     db.commit()
#     return {"message": "Item removed from cart"}
#
#
# @router.delete("/cart/")
# async def clear_cart(
#         db: Session = Depends(get_db),
#         token: str = Header(...),
# ):
#     user = await get_user_from_service(token)
#     cart = db.query(Cart).filter(Cart.user_id == user["id"]).first()
#     if not cart:
#         raise HTTPException(status_code=404, detail="Cart not found")
#
#     db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
#     db.commit()
#     return {"message": "Cart cleared"}
#
#
# @router.post("/cart/checkout/")
# async def checkout_cart(
#         order_data: OrderCreate,
#         db: Session = Depends(get_db),
#         token: str = Header(...),
# ):
#     user = await get_user_from_service(token)
#     cart = db.query(Cart).filter(Cart.user_id == user["id"]).first()
#     if not cart or not cart.cart_items:
#         raise HTTPException(status_code=400, detail="Cart is empty")
#
#     order = await create_order_in_order_service(cart, user, order_data)
#
#     db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
#     db.commit()
#
#     return {"message": "Order created", "order_id": order["id"]}
