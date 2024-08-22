from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field
from schemas.event import EventResponseSchema


class BetSchema(BaseModel):
    amount: Decimal = Field(ge=Decimal("0.01"), le=Decimal("100_000_000.00"), decimal_places=2)
    event_id: UUID


class BetResponseSchema(BaseModel):
    id: UUID
    amount: Decimal = Field(ge=Decimal("0.01"), le=Decimal("100_000_000.00"), decimal_places=2)
    event: EventResponseSchema
