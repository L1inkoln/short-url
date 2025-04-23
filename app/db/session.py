from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


engine: AsyncEngine = create_async_engine(settings.DATABASE_URL, echo=True)

AsyncSessionLocal: sessionmaker[AsyncSession] = sessionmaker(  # type: ignore
    bind=engine, class_=AsyncSession, expire_on_commit=False  # type: ignore
)


# DI FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
