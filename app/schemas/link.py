from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional


class LinkBase(BaseModel):
    original_url: HttpUrl


class LinkResponse(LinkBase):
    short_code: str


class LinkCreate(LinkBase):
    custom_alias: Optional[str] = Field(
        None,
        min_length=3,
        max_length=10,
        description="Необязательный кастомный короткий код (3-10 символов)",
    )


class LinkStats(LinkBase):
    short_code: str = Field(default=..., min_length=1, max_length=10)
    clicks: int = Field(default=..., ge=0)
    created_at: datetime
    last_clicked_at: Optional[datetime]

    class Config:
        from_attributes = True
