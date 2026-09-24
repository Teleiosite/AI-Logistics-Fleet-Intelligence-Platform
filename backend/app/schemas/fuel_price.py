from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class FuelPriceCreate(BaseModel):
    region: str
    fuel_type: str = "diesel"
    price_per_liter: Decimal


class FuelPriceRead(FuelPriceCreate):
    id: str
    company_id: str
    recorded_at: datetime

    model_config = {"from_attributes": True}
