from datetime import datetime
import secrets
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.db.models import Link


# Создание короткой ссылки и проверка на существующий короткий код
async def create_link(
    db: AsyncSession, original_url: str, custom_alias: str | None = None
) -> Link:
    if custom_alias:
        short_code = custom_alias
    else:
        short_code = secrets.token_urlsafe(6)[:6]

    # Проверка на уникальность
    result = await db.execute(select(Link).where(Link.short_code == short_code))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(
            status_code=400, detail="Короткий код уже занят. Выберите другой."
        )

    link = Link(original_url=original_url, short_code=short_code, clicks=0)
    db.add(link)
    await db.commit()
    await db.refresh(link)
    return link


# Функция которая возвращает оригинальную ссылку для редиректа
async def get_link_and_increment_clicks(
    db: AsyncSession, short_code: str
) -> Link | None:
    result = await db.execute(
        update(Link)
        .where(Link.short_code == short_code)
        .values(clicks=Link.clicks + 1, last_clicked_at=datetime.utcnow())
        .returning(Link)
    )
    await db.commit()
    return result.scalars().first()


# Просмотр статистики для короткой ссылки
async def get_link_info(db: AsyncSession, short_code: str) -> Link | None:
    result = await db.execute(select(Link).where(Link.short_code == short_code))
    return result.scalars().first()
