import pytest
from app.services.link_service import create_link, get_link_and_increment_clicks


@pytest.mark.asyncio
async def test_create_link(mock_db_session):
    test_url = "https://example.com"
    result = await create_link(mock_db_session, test_url)

    assert result.original_url == test_url
    assert len(result.short_code) > 0

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_awaited_once()
    mock_db_session.refresh.assert_awaited_once_with(result)


@pytest.mark.asyncio
async def test_get_and_increment_clicks(mock_db_session):
    updated_link = await get_link_and_increment_clicks(mock_db_session, "test123")
    # Проверяем что:
    # 1. Функция вернула объект Link
    # 2. Был выполнен UPDATE запрос
    # 3. Был вызван commit
    assert updated_link is not None
    mock_db_session.execute.assert_awaited_once()
    mock_db_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_nonexistent_link(mock_db_session_empty):
    result = await get_link_and_increment_clicks(mock_db_session_empty, "nonexistent")
    assert result is None
