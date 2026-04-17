from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import AuthContext, require_permissions
from app.db.session import get_db
from app.schemas.invoice import InvoiceCreate, InvoiceRead
from app.services.crud import auto_match_invoice, create_invoice, list_invoices

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post("", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
def create_invoice_endpoint(
    payload: InvoiceCreate,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permissions("write")),
) -> InvoiceRead:
    invoice = create_invoice(db, auth.company_id, payload)
    return InvoiceRead.model_validate(invoice)


@router.get("", response_model=list[InvoiceRead])
def list_invoices_endpoint(
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permissions("read")),
) -> list[InvoiceRead]:
    return [InvoiceRead.model_validate(item) for item in list_invoices(db, auth.company_id)]


@router.post("/{invoice_id}/auto-match")
def auto_match_invoice_endpoint(
    invoice_id: str,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permissions("approve")),
) -> dict[str, int]:
    return auto_match_invoice(db, auth.company_id, invoice_id)
