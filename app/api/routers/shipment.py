from fastapi import APIRouter, HTTPException, status
from app.api.dependencies import SellerDep, ShipmentServiceDep
from app.database.models import Shipment
from app.api.schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate

router = APIRouter(
    prefix="/shipment",
    tags=['Shipment'],
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=ShipmentRead)
async def get_shipment(id: int, _: SellerDep, service: ShipmentServiceDep):
    return await service.get(id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def submit_shipment(shipment: ShipmentCreate, service: ShipmentServiceDep, seller: SellerDep) -> Shipment:
    return await service.add(shipment)


@router.patch("/", response_model=ShipmentRead)
async def update_shipment(id: int, shipment_update: ShipmentUpdate, service: ShipmentServiceDep):
    update = shipment_update.model_dump(exclude_none=True)
    
    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update"
        )
        
    shipment = await service.update(id, update)

    return shipment


@router.delete("/")
async def delete_shipment(id: int, service: ShipmentServiceDep) -> dict[str, str]:
    await service.delete(id)
    return {"detail": f"Shipment with id #{id} was successfully deleted."}
