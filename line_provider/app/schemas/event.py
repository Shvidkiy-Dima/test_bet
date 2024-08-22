from decimal import Decimal
from uuid import UUID

from enums.event import EventEnum
from pydantic import BaseModel, Field, NaiveDatetime


class EventSchema(BaseModel):
    id: UUID
    winning_odds: Decimal = Field(ge=Decimal("0.01"), decimal_places=2)
    deadline: NaiveDatetime
    status: EventEnum
