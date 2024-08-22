import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path

from httpx import AsyncClient
from models.bet import Bet
from models.event import Event
from sqlalchemy import select

app_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(app_dir))

import pytest
from enums.event import EventEnum
from main import app
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio()
async def test_event(session: AsyncSession):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        event_id = str(uuid.uuid4())
        deadline_event_id = str(uuid.uuid4())

        # create event
        data = {
            "id": event_id,
            "winning_odds": "2.01",
            "deadline": str(datetime.now() + timedelta(days=1)),
            "status": EventEnum.UNFINISHED,
            "date": str(datetime.now()),
        }
        response = await ac.post("/api/v1/callback/event/", json=data)
        assert response.status_code == 200
        assert len((await session.execute(select(Event))).scalars().all()) == 1

        # expired message
        data = {
            "id": event_id,
            "winning_odds": "2.01",
            "deadline": str(datetime.now() + timedelta(days=1)),
            "status": EventEnum.UNFINISHED,
            "date": str(datetime.now() - timedelta(days=1)),
        }

        response = await ac.post("/api/v1/callback/event/", json=data)
        assert response.status_code == 200
        assert len((await session.execute(select(Event))).scalars().all()) == 1

        # change status
        data = {
            "id": event_id,
            "winning_odds": "2.01",
            "deadline": str(datetime.now() + timedelta(days=1)),
            "status": EventEnum.FIRST_WIN,
            "date": str(datetime.now()),
        }

        response = await ac.post("/api/v1/callback/event/", json=data)
        assert response.status_code == 200
        assert len((await session.execute(select(Event))).scalars().all()) == 1
        event = (await session.execute(select(Event))).scalars().first()
        assert event.status == EventEnum.FIRST_WIN

        # event deadline
        data = {
            "id": deadline_event_id,
            "winning_odds": "2.01",
            "deadline": str(datetime.now() - timedelta(days=1)),
            "status": EventEnum.UNFINISHED,
            "date": str(datetime.now()),
        }

        response = await ac.post("/api/v1/callback/event/", json=data)
        assert response.status_code == 200
        assert len((await session.execute(select(Event))).scalars().all()) == 2

        # event list
        response = await ac.get("/api/v1/event/")
        assert response.status_code == 200
        assert len(response.json()) == 1

        # bet
        data = {
            "event_id": event_id,
            "amount": "1222.00",
        }
        response = await ac.post("/api/v1/bet/", json=data)
        assert response.status_code == 200
        assert len((await session.execute(select(Bet))).scalars().all()) == 1

        # bet not exists event
        data = {
            "event_id": str(uuid.uuid4()),
            "amount": "1222.00",
        }
        response = await ac.post("/api/v1/bet/", json=data)
        assert response.status_code == 404

        # bet deadline
        data = {
            "event_id": deadline_event_id,
            "amount": "1222.00",
        }
        response = await ac.post("/api/v1/bet/", json=data)
        assert response.status_code == 400
