from decimal import Decimal

from pydantic import BaseModel


class InvoiceCreate(BaseModel):
    transporter_id: str | None = None
    invoice_number: str
    total_amount: Decimal


class InvoiceRead(InvoiceCreate):
    id: str
    company_id: str
    discrepancy_count: int
    status: str

    model_config = {"from_attributes": True}
