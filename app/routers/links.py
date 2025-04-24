from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.link import LinkCreate, LinkStats, LinkResponse
from app.services.link_service import (
    create_link,
    get_link_and_increment_clicks,
    get_link_info,
)
from app.db.session import get_db


router = APIRouter(prefix="/links", tags=["Links"])


@router.post("/", response_model=LinkResponse)
async def create_short_link(link_data: LinkCreate, db: AsyncSession = Depends(get_db)):
    link = await create_link(db, str(link_data.original_url), link_data.custom_alias)
    return link


@router.get("/r/{short_code}")
async def redirect_link(short_code: str, db: AsyncSession = Depends(get_db)):
    link = await get_link_and_increment_clicks(db, short_code)
    if not link:
        raise HTTPException(status_code=404)
    return RedirectResponse(url=link.original_url)  # 307 редирект


# Получение информации о ссылке
@router.get("/{short_code}/info", response_model=LinkStats)
async def get_info(short_code: str, db: AsyncSession = Depends(get_db)):
    link = await get_link_info(db, short_code)
    if not link:
        raise HTTPException(status_code=404)
    return link
