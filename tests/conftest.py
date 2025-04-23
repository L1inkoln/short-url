import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from app.db.models import Link


@pytest.fixture
def mock_db_session():
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_link = Link(
        id=1,
        original_url="https://example.com",
        short_code="test123",
        clicks=5,
        created_at=datetime.utcnow(),
    )
    mock_result.scalars.return_value.first.return_value = mock_link
    mock_db.execute = AsyncMock(return_value=mock_result)

    mock_db.commit = AsyncMock()
    mock_db.add = AsyncMock()
    mock_db.refresh = AsyncMock()
    return mock_db


@pytest.fixture
def mock_db_session_empty():
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db.execute = AsyncMock(return_value=mock_result)
    return mock_db
