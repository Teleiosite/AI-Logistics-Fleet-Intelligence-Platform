from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.dependencies import AuthContext, require_permission
from app.db.session import get_db
from app.schemas.invoice import InvoiceCreate, InvoiceRead, InvoiceUploadText
from app.services.crud import auto_match_invoice, create_invoice, create_invoice_from_text, generate_dispute_memo, list_invoices
from app.services.invoice_ocr import extract_invoice_document, extract_invoice_image

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


@router.post("/upload", response_model=InvoiceRead)
async def upload_invoice_document_endpoint(
    file: UploadFile = File(...),
    transporter_id: str | None = None,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("invoices", "write")),
) -> InvoiceRead:
    if file.content_type not in {"application/pdf", "text/plain", "image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(status_code=415, detail="Unsupported invoice document type")
    content = await file.read()
    try:
        if file.content_type.startswith("image/"):
            extracted = extract_invoice_image(file.filename or "invoice-image", content)
        else:
            extracted = extract_invoice_document(file.filename or "invoice.txt", content)
        raw_text = f"Invoice Number: {extracted['invoice_number']}\n" + "\n".join(
            f"{item['description']} {item['amount']}" for item in extracted["line_items"]
        )
        payload = InvoiceUploadText(transporter_id=transporter_id, raw_text=raw_text)
        invoice = create_invoice_from_text(db, auth.company_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
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
