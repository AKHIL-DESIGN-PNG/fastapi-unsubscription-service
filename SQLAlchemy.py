from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
DATABASE_URL = f"postgresql+asyncpg://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', 'postgres')}@localhost:5432/mydatabase"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, scoped_session
from sqlalchemy.orm.session import sessionmaker
import os

DATABASE_URL = f"postgresql+asyncpg://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', 'postgres')}@localhost:5432/mydatabase"

engine = create_async_engine(DATABASE_URL, echo=True)

Base = declarative_base()

def get_session():
    session = scoped_session(sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False))
    return session

async def get_db():
    session = get_session()
    try:
        yield session
    finally:
        await session.close()
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
