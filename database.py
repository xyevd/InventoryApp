from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker
from collections.abc import AsyncGenerator

DATABASE_URL = "postgresql+asyncpg://qsddvfbbicloud.com@localhost:5432/inventorydb"

engine = create_async_engine(DATABASE_URL, echo=True)

# Session fabric
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,  # не обнулять объекты после коммита
)

# models base class (models/*.py)
Base = declarative_base()

# Зависимость для FastAPI — использовать в эндпоинтах
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
