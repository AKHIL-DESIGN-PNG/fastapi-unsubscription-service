

import os
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DB_USER =os.getenv("postgres", "postgres")
DB_PASSWORD = os.getenv("postgres", "postgres")

DATABASE_URL =f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@localhost:5432/unsubscribe_service"
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session
        await session.close() 
