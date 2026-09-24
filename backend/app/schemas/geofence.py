from decimal import Decimal

from pydantic import BaseModel, Field


class GeofenceCreate(BaseModel):
    name: str
    latitude: Decimal = Field(ge=-90, le=90)
    longitude: Decimal = Field(ge=-180, le=180)
    radius_meters: Decimal = Field(gt=0, le=100000)


class GeofenceRead(GeofenceCreate):
    id: str
    company_id: str
    is_active: bool

    model_config = {"from_attributes": True}
