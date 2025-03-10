from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from fastapi_users.authentication import BearerTransport
from app.config import SECRETJWT

cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRETJWT, lifetime_seconds=3600)


bearer_transport = BearerTransport(tokenUrl="api/auth/jwt/login")

auth_backend = AuthenticationBackend(
    name="jwt",
    # transport=cookie_transport,
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
