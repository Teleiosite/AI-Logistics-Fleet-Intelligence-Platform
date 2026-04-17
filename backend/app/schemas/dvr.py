from decimal import Decimal

from pydantic import BaseModel


class DVRCreate(BaseModel):
    shipment_id: str
    dvr_number: str
    variance_type: str
    description: str
    financial_impact: Decimal | None = None


class DVRRead(DVRCreate):
    id: str
    company_id: str
    status: str

    model_config = {"from_attributes": True}
