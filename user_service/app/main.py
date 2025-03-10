from fastapi import Depends, FastAPI
from fastapi_users import FastAPIUsers

from app.auth import auth_backend
from app.models import User
from app.manager import get_user_manager
from app.schemas.schemas import UserRead, UserCreate

app = FastAPI()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# Роуты авторизации
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/auth",
    tags=["auth"],
)

# Пример защищенного и открытого роутов
current_user = fastapi_users.current_user()

@app.post("/api/auth/jwt/verify-token")
async def verify_token(user=Depends(fastapi_users.current_user(active=True))):
    return user  # Вернуть информацию о пользователе, если токен валиден
@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return {"message": f"Hello, {user.name}"}


@app.get("/unprotected-route")
def unprotected_route():
    return {"message": "Hello, anonym"}
