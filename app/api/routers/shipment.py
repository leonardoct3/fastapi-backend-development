from uuid import UUID
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from app.api.dependencies import DeliveryPartnerDep, SellerDep, ShipmentServiceDep
from app.api.schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate
from app.utils.email_util import TEMPLATE_DIR

router = APIRouter(
    prefix="/shipment",
    tags=["Shipment"],
)

templates = Jinja2Templates(
    TEMPLATE_DIR
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=ShipmentRead)
async def get_shipment(id: UUID, service: ShipmentServiceDep):
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )

    return shipment


### Tracking details of shipment
@router.get("/track")
async def get_tracking(request: Request, id: UUID, service: ShipmentServiceDep):
    shipment = await service.get(id)

    context = shipment.model_dump()
    context["status"] = shipment.status
    context["partner"] = shipment.delivery_partner.name
    shipment.timeline.reverse()
    context["timeline"] = shipment.timeline

    return templates.TemplateResponse(
        request=request,
        name="track.html",
        context=context
    )

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
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided to update"
        )

    return await service.update(id, shipment_update, partner)


@router.get("/cancel", response_model=ShipmentRead)
async def cancel_shipment(
    id: UUID, seller: SellerDep, service: ShipmentServiceDep
) -> dict[str, str]:
    return await service.cancel(id, seller)
