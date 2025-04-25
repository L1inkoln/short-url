from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from app.core.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker


engine: AsyncEngine = create_async_engine(settings.DATABASE_URL, echo=True)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


# DI FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
