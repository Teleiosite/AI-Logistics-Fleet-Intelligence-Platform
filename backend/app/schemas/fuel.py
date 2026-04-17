from decimal import Decimal

from pydantic import BaseModel


class FuelLogCreate(BaseModel):
    vehicle_id: str
    shipment_id: str | None = None
    quantity_liters: Decimal
    price_per_liter: Decimal
    odometer_reading_km: Decimal | None = None


class FuelLogRead(BaseModel):
    id: str
    company_id: str
    vehicle_id: str
    quantity_liters: Decimal
    price_per_liter: Decimal
    total_cost: Decimal
    is_anomaly: bool
    anomaly_reason: str | None

    model_config = {"from_attributes": True}
