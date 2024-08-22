from datetime import datetime

from event_manager import EventManager
from fastapi import APIRouter
from schemas.event import EventSchema

router = APIRouter()


@router.post("/")
async def create_event(data_in: EventSchema):
    message = data_in.model_dump()
    message["date"] = datetime.utcnow()

    await EventManager.put_event(message=message)
