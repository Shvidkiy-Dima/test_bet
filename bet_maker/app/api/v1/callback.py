from api import dependences
from fastapi import APIRouter, Depends, Response
from models.event import Event
from schemas.event import EventSchema
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

from loguru import logger


@router.post("/event/")
async def new_event(data_in: EventSchema, session: AsyncSession = Depends(dependences.get_db)):
    logger.info(f"NEW EVENT {data_in}")

    event = (await session.execute(select(Event).where(Event.id == data_in.id).with_for_update())).scalar()
    if event is None:
        await session.execute(
            insert(Event).values({
                "updated_at": data_in.date,
                "created_at": data_in.date,
                **data_in.model_dump(exclude_unset=True, exclude={"date"}),
            })
        )

        await session.commit()
        logger.info(f"CREATE EVENT {data_in}")

    elif data_in.date > event.updated_at:
        await session.execute(
            update(Event)
            .where(Event.id == data_in.id)
            .values(winning_odds=data_in.winning_odds, status=data_in.status, updated_at=data_in.date)
        )

        await session.commit()
        logger.info(f"UPDATE EVENT {data_in}")

    return Response(status_code=200)
