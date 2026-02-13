from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from app.api.dependencies import DeliveryPartnerDep, SellerDep, ShipmentServiceDep
from app.api.schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate

router = APIRouter(
    prefix="/shipment",
    tags=["Shipment"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=ShipmentRead)
async def get_shipment(id: UUID, _: SellerDep, service: ShipmentServiceDep):
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )

    return shipment


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShipmentRead)
async def submit_shipment(
    shipment: ShipmentCreate, service: ShipmentServiceDep, seller: SellerDep
):
    return await service.add(shipment, seller)


@router.patch("/", response_model=ShipmentRead)
async def update_shipment(
    id: UUID,
    shipment_update: ShipmentUpdate,
    service: ShipmentServiceDep,
    partner: DeliveryPartnerDep,
):
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="No data provided to update"
        )

    return await service.update(id, shipment_update, partner)


@router.delete("/")
async def delete_shipment(id: UUID, service: ShipmentServiceDep) -> dict[str, str]:
    await service.delete(id)
    return {"detail": f"Shipment with id #{id} was successfully deleted."}
