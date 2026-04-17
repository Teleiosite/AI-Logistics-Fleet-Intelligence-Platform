from decimal import Decimal

from pydantic import BaseModel


class VehicleCreate(BaseModel):
    vehicle_number: str
    license_plate: str
    vehicle_type: str = "truck"
    tank_capacity_liters: Decimal | None = None


class VehicleRead(VehicleCreate):
    id: str
    company_id: str
    status: str

    model_config = {"from_attributes": True}


class DriverCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    license_number: str


class DriverRead(DriverCreate):
    id: str
    company_id: str
    status: str

    model_config = {"from_attributes": True}


class TransporterCreate(BaseModel):
    name: str
    contact_person: str | None = None
    phone: str | None = None
    email: str | None = None


class TransporterRead(TransporterCreate):
    id: str
    company_id: str
    status: str

    model_config = {"from_attributes": True}
