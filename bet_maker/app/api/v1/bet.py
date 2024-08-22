from datetime import datetime
from typing import List

from api import dependences
from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from models.bet import Bet
from models.event import Event
from schemas.bet import BetResponseSchema, BetSchema
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

router = APIRouter()


@router.post("/", response_model=BetResponseSchema)
async def create_bet(data_in: BetSchema, session: AsyncSession = Depends(dependences.get_db)):
    event = (await session.execute(select(Event).where(Event.id == data_in.event_id))).scalars().first()

    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"event {data_in.event_id} not found")

    if datetime.utcnow() > event.deadline:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"the deadline for this event {data_in.event_id} has arrived",
        )

    logger.info(f"NEW BET {data_in}")
    bet = (
        (
            await session.execute(
                insert(Bet).values(**data_in.model_dump()).returning(Bet).options(joinedload(Bet.event, innerjoin=True))
            )
        )
        .scalars()
        .first()
    )
    await session.commit()
    return BetResponseSchema.model_validate(bet, from_attributes=True)


@router.get("/", response_model=List[BetResponseSchema])
async def get_bets(session: AsyncSession = Depends(dependences.get_db)):
    bets = (await session.execute(select(Bet).options(joinedload(Bet.event, innerjoin=True)))).scalars().all()
    return bets
