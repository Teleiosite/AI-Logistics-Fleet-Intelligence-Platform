from pydantic import BaseModel


class ShipmentCreate(BaseModel):
    shipment_number: str
    customer_name: str
    pickup_address: str
    delivery_address: str
    vehicle_id: str | None = None
    driver_id: str | None = None


class ShipmentStatusUpdate(BaseModel):
    status: str
    notes: str | None = None


class ShipmentPODUpdate(BaseModel):
    proof_of_delivery_url: str | None = None
    delivery_signature_url: str | None = None


class ShipmentRead(BaseModel):
    id: str
    company_id: str
    shipment_number: str
    customer_name: str
    pickup_address: str
    delivery_address: str
    vehicle_id: str | None = None
    driver_id: str | None = None
    status: str
    proof_of_delivery_url: str | None = None
    delivery_signature_url: str | None = None

    model_config = {"from_attributes": True}
