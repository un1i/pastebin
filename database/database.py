from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.config import POSTGRES_DSN, SYNC_DSN
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from database.models import User

DATABASE_URL = POSTGRES_DSN

SYNC_URL = SYNC_DSN

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


def get_connect():
    return create_engine(SYNC_URL).connect()


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

