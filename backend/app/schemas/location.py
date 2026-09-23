from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class LocationPingCreate(BaseModel):
    vehicle_id: str
    latitude: Decimal = Field(ge=-90, le=90)
    longitude: Decimal = Field(ge=-180, le=180)
    recorded_at: datetime | None = None


class LocationPingRead(LocationPingCreate):
    id: str
    company_id: str

    model_config = {"from_attributes": True}
