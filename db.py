# backend/db.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@postgres:5432/{os.getenv('POSTGRES_DB')}"
)

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session
