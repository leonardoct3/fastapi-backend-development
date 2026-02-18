from random import randint
from app.database.models import Shipment, ShipmentEvent, ShipmentStatus
from app.database.redis import add_shipment_verification_code
from app.services.base import BaseService
from app.services.notification import NotificationService

class ShipmentEventService(BaseService):
    def __init__(self, session, tasks):
        super().__init__(ShipmentEvent, session)
        self.notification_service = NotificationService(tasks)

    async def add(
        self,
        shipment: Shipment,
        location: int = None,
        status: ShipmentStatus = None,
        description: str = None,
    ):
        if not location or not status:
            last_event = await self.get_latest_event(shipment)
            location = location if location else last_event.location
            status = status if status else last_event.status

        new_event = ShipmentEvent(
            location=location,
            status=status,
            description=description if description else self._generate_description(status, location),
            shipment_id=shipment.id
        )
        
        await self._notify(shipment, status)
        
        return await self._add(new_event)
    
    async def get_latest_event(self, shipment: Shipment):
        timeline = sorted(
            shipment.timeline or [],
            key=lambda item: item.created_at,
        )

        return timeline[-1] if timeline else None

    def _generate_description(self, status: ShipmentStatus, location: int):
        match status:
            case ShipmentStatus.placed:
                return "assigned delivery partner"
            case ShipmentStatus.delivered:
                return "successfully delivered"
            case ShipmentStatus.out_for_delivery:
                return "shipment out for delivery"
            case ShipmentStatus.cancelled:
                return "cancelled by the seller"
            case _:
                return f"scanned at {location}"

    async def _notify(self, shipment: Shipment, status: ShipmentStatus):

        if status == ShipmentStatus.in_transit:
            return

        subject: str
        template_name: str
        context: dict = {}

        match status:
            case ShipmentStatus.placed:
                subject="Your order is shipped 🚛"
                template_name = "mail_placed.html"
            case ShipmentStatus.out_for_delivery:
                subject="Your order is out for delivery 🛵"
                template_name = "mail_out_for_delivery.html"

                code = randint(100_000, 999_999)
                add_shipment_verification_code(shipment.id, code)

                if shipment.client_contact_phone:
                    try:
                        self.notification_service.send_sms(
                            to=shipment.client_contact_phone,
                            body=f"Your order is arriving soon! Share the {code} code with your"
                            "delivery executive to receive your package."
                        )
                    except Exception:
                        context["verification_code"] = code

                else:
                    context["verification_code"] = code

            case ShipmentStatus.cancelled:
                subject="Your order was cancelled ❌"
                template_name = "mail_cancelled.html"
            case ShipmentStatus.delivered:
                subject="Your order was delivered ✅"
                template_name = "mail_delivered.html"
        
        context["id"] = shipment.id
        context["seller"] = shipment.seller.name
        context["partner"] = shipment.delivery_partner.name

        await self.notification_service.send_message_with_template(
            recipients=[shipment.client_contact_email],
            subject=subject,
            context=context,
            template_name=template_name
        )