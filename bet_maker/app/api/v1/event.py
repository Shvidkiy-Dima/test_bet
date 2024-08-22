from datetime import datetime
from typing import List

from api import dependences
from fastapi import APIRouter, Depends
from models.event import Event
from schemas.event import EventResponseSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/", response_model=List[EventResponseSchema])
async def get_events(session: AsyncSession = Depends(dependences.get_db)):
    return (await session.execute(select(Event).where(Event.deadline > datetime.utcnow()))).scalars().all()
