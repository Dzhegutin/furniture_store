from typing import Optional, List

from fastapi_users import IntegerIDMixin, BaseUserManager, schemas, models, exceptions

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.database import get_db, SessionLocal
from app.config import SECRETMANAGER


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRETMANAGER
    verification_token_secret = SECRETMANAGER

    async def on_after_register(self, user: User, request: Optional[Request] = None,
                                db: AsyncSession = None):
        print(f"User {user.id} has registered.")

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)
        async with SessionLocal() as db:
            await self.on_after_register(created_user, request, db)

        return created_user


async def get_user_manager(user_db=Depends(get_db)):
    yield UserManager(user_db)
