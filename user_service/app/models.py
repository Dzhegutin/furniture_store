from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base, get_db


class User(SQLAlchemyBaseUserTable[int], Base):
    # email, hashed_password, is_active, is_superuser, is_verified GET from SQLAlchemyBaseUserTable

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    last_name = Column(String)
    birthday = Column(Date)
    phone_number = Column(String)
    user_city = Column(String)
    address = Column(String)