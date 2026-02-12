from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import SQLModel
from fastapi import Depends
from sqlalchemy.orm import sessionmaker

from app.config.config import db_settings

engine = create_async_engine(
    # database type/dialect and file name
    url=db_settings.POSTGRES_URL,
    echo=True
)

async def create_database_tables():
    async with engine.begin() as connection:
        from .models import Shipment
        await connection.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]