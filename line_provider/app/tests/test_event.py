import sys
from pathlib import Path

app_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(app_dir))

import uuid
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch

import pytest
from enums.event import EventEnum
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio()
async def test_event():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        event_id = str(uuid.uuid4())
        data = {
            "id": event_id,
            "winning_odds": "2.01",
            "deadline": str(datetime.now() + timedelta(days=1)),
            "status": EventEnum.UNFINISHED,
        }
        with patch("event_manager.EventManager.put_event", side_effect=AsyncMock()) as mock:
            response = await ac.post("/api/v1/event/", json=data)
            assert response.status_code == 200
            assert mock.call_count == 1
