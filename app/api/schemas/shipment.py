from random import randint
from uuid import UUID
from pydantic import BaseModel, Field
from app.database.models import ShipmentEvent, ShipmentStatus
from datetime import datetime

def random_destination():
    return randint(11000, 11999)

class BaseShipment(BaseModel):
    content: str
    weight: float = Field(le=25)
    destination: int

class ShipmentRead(BaseShipment):
    id: UUID
    timeline: list[ShipmentEvent]
    estimated_delivery: datetime


class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    location: int | None = Field(default=None)
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)
    description: str | None = Field(default=None)
