from datetime import datetime
from enum import Enum
from pydantic import EmailStr
from sqlmodel import Column, Field, Relationship, SQLModel
from uuid import uuid4, UUID
from sqlalchemy.dialects import postgresql
from sqlalchemy import ARRAY, INTEGER

class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"

class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4(),
            primary_key=True
        )
    )
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime
    
    seller_id: UUID = Field(foreign_key="seller.id")
    seller: "Seller" = Relationship(back_populates="shipments", sa_relationship_kwargs={"lazy": "selectin"})

    delivery_partner_id : UUID = Field(foreign_key="delivery_partner.id")

    delivery_partner : "DeliveryPartner" = Relationship(back_populates="shipments", sa_relationship_kwargs={"lazy": "selectin"})

    created_at : datetime = Field(sa_column=Column(
        postgresql.TIMESTAMP,
        default=datetime.now()
    ))

class User(SQLModel):
    name: str
    email: EmailStr
    password_hash: str

class Seller(User, table=True):
    __tablename__ = "seller"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4(),
            primary_key=True
        )
    )

    shipments : list[Shipment] = Relationship(back_populates="seller", sa_relationship_kwargs={"lazy": "selectin"})

    created_at : datetime = Field(sa_column=Column(
        postgresql.TIMESTAMP,
        default=datetime.now()
    ))

class DeliveryPartner(User, table=True):
    __tablename__ = "delivery_partner"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4(),
            primary_key=True
        )
    )
    
    serviceable_zip_codes: list[int] = Field(
        sa_column=Column(ARRAY(INTEGER))
    )

    max_handling_capacity: int

    shipments : list["Shipment"] = Relationship(back_populates="delivery_partner", sa_relationship_kwargs={"lazy": "selectin"})

    created_at : datetime = Field(sa_column=Column(
        postgresql.TIMESTAMP,
        default=datetime.now()
    ))