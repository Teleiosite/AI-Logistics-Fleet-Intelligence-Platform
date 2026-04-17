from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import AuthContext, require_permission
from app.db.session import get_db
from app.schemas.invoice import InvoiceCreate, InvoiceRead, InvoiceUploadText
from app.services.crud import auto_match_invoice, create_invoice, create_invoice_from_text, generate_dispute_memo, list_invoices

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post("", response_model=InvoiceRead)
def create_invoice_endpoint(
    payload: InvoiceCreate,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("invoices", "write")),
) -> InvoiceRead:
    invoice = create_invoice(db, auth.company_id, payload)
    return InvoiceRead.model_validate(invoice)


@router.post("/upload-text", response_model=InvoiceRead)
def upload_invoice_text_endpoint(
    payload: InvoiceUploadText,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("invoices", "write")),
) -> InvoiceRead:
    invoice = create_invoice_from_text(db, auth.company_id, payload)
    return InvoiceRead.model_validate(invoice)


@router.get("", response_model=list[InvoiceRead])
def list_invoices_endpoint(
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("invoices", "read")),
) -> list[InvoiceRead]:
    return [InvoiceRead.model_validate(item) for item in list_invoices(db, auth.company_id)]


@router.post("/{invoice_id}/auto-match")
def auto_match_invoice_endpoint(
    invoice_id: str,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("invoices", "approve")),
) -> dict[str, int]:
    return auto_match_invoice(db, auth.company_id, invoice_id)


@router.get("/{invoice_id}/dispute-memo")
def dispute_memo_endpoint(
    invoice_id: str,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("invoices", "approve")),
) -> dict[str, str]:
    return {"memo": generate_dispute_memo(db, auth.company_id, invoice_id)}
