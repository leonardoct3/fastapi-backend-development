from random import randint
from pydantic import BaseModel, Field
from app.database.models import ShipmentStatus
from datetime import datetime

def random_destination():
    return randint(11000, 11999)

class BaseShipment(BaseModel):
    content: str
    weight: float = Field(le=25)
    destination: int

class ShipmentRead(BaseShipment):
    status : ShipmentStatus
    estimated_delivery: datetime


class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = None
    estimated_delivery: datetime | None = None
