from app.services.shipment import ShipmentService
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

async def get_shipment_service(session: SessionDep):
    return ShipmentService(session)

ServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]