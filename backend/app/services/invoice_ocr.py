import re
import base64
import json
from urllib.request import Request, urlopen
from decimal import Decimal
from io import BytesIO

from pypdf import PdfReader

from app.core.config import get_settings


LINE_ITEM_PATTERN = re.compile(r"(?P<desc>[A-Za-z0-9\-\s]+)\s+(?P<amount>\d+(?:\.\d{1,2})?)")


def extract_invoice_fields(raw_text: str) -> dict[str, object]:
    invoice_number_match = re.search(r"invoice\s*(?:no|number)[:\s]+([A-Za-z0-9\-_/]+)", raw_text, flags=re.IGNORECASE)
    invoice_number = invoice_number_match.group(1) if invoice_number_match else "UNKNOWN"

    line_items: list[dict[str, object]] = []
    total = Decimal("0")
    for match in LINE_ITEM_PATTERN.finditer(raw_text):
        amount = Decimal(match.group("amount"))
        line_items.append({"description": match.group("desc").strip(), "amount": amount})
        total += amount

    return {
        "invoice_number": invoice_number,
        "line_items": line_items,
        "total_amount": total.quantize(Decimal("0.01")),
    }


def extract_invoice_document(filename: str, content: bytes) -> dict[str, object]:
    """Extract text from UTF-8 documents and text-based PDFs before parsing fields."""
    if not content:
        raise ValueError("Invoice document is empty")
    if filename.lower().endswith(".pdf"):
        try:
            reader = PdfReader(BytesIO(content))
            raw_text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as exc:
            raise ValueError("Unable to read PDF invoice") from exc
    else:
        try:
            raw_text = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Unsupported document encoding; upload a text-based PDF or UTF-8 file") from exc
    if not raw_text.strip():
        raise ValueError("Invoice document contains no extractable text")
    result = extract_invoice_fields(raw_text)
    result["source_filename"] = filename
    result["extraction_method"] = "pdf_text" if filename.lower().endswith(".pdf") else "utf8_text"
    return result


def extract_invoice_image(filename: str, content: bytes) -> dict[str, object]:
    """Delegate image OCR to a configured provider using a small JSON contract."""
    settings = get_settings()
    if not settings.ocr_provider_url:
        raise ValueError("OCR_PROVIDER_URL is required for image invoice ingestion")
    body = json.dumps({
        "filename": filename,
        "content_base64": base64.b64encode(content).decode("ascii"),
    }).encode()
    headers = {"Content-Type": "application/json"}
    if settings.ocr_provider_api_key:
        headers["Authorization"] = "Bearer " + settings.ocr_provider_api_key
    try:
        request = Request(settings.ocr_provider_url, data=body, headers=headers, method="POST")
        with urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise ValueError("Configured OCR provider could not process the invoice") from exc
    raw_text = result.get("text")
    if not isinstance(raw_text, str) or not raw_text.strip():
        raise ValueError("OCR provider returned no text")
    extracted = extract_invoice_fields(raw_text)
    extracted["source_filename"] = filename
    extracted["extraction_method"] = "external_image_ocr"
    return extracted
