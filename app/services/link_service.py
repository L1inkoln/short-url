from datetime import datetime
import secrets
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from app.db.models import Link


async def create_link(
    db: AsyncSession, original_url: str, custom_alias: str | None = None
) -> Link:
    if custom_alias:
        short_code = custom_alias
    else:
        short_code = secrets.token_urlsafe(6)[:6]

    link = Link(original_url=original_url, short_code=short_code, clicks=0)
    db.add(link)
    await db.commit()
    await db.refresh(link)
    return link


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
