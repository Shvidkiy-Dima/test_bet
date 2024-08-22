from enums.event import EventEnum
from models.base import BaseModel
from sqlalchemy import DECIMAL, UUID, DateTime, Enum
from sqlalchemy.orm import mapped_column, relationship


class Event(BaseModel):
    id = mapped_column(UUID, primary_key=True, index=True, nullable=False)
    winning_odds = mapped_column(DECIMAL(12, 2), nullable=False)
    deadline = mapped_column(DateTime, nullable=False)
    status = mapped_column(Enum(EventEnum), nullable=False)
    bets = relationship("Bet", back_populates="event")
