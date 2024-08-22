from uuid import uuid4

from models.base import BaseModel
from sqlalchemy import DECIMAL, UUID, ForeignKey
from sqlalchemy.orm import mapped_column, relationship


class Bet(BaseModel):
    id = mapped_column(UUID, primary_key=True, index=True, nullable=False, default=uuid4)
    amount = mapped_column(DECIMAL(12, 2), nullable=False)
    event_id = mapped_column(UUID, ForeignKey("event.id"), nullable=False, index=True)

    event = relationship("Event", back_populates="bets")
