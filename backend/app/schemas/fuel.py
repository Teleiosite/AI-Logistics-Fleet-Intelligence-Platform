from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class FuelLogCreate(BaseModel):
    vehicle_id: str
    shipment_id: str | None = None
    quantity_liters: Decimal
    price_per_liter: Decimal
    odometer_reading_km: Decimal | None = None
    station_name: str | None = None


class FuelLogRead(BaseModel):
    id: str
    company_id: str
    vehicle_id: str
    quantity_liters: Decimal
    price_per_liter: Decimal
    total_cost: Decimal
    station_name: str | None = None
    fuel_efficiency_lkm: Decimal | None = None
    is_anomaly: bool
    anomaly_reason: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
