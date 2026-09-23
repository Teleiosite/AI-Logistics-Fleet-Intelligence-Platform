from app.services.invoice_ocr import extract_invoice_document, extract_invoice_fields


def test_extract_invoice_fields_parses_invoice_number_and_total() -> None:
    text = "Invoice Number: INV-2026-001\nRoute Lagos-Abuja 1200.50\nHandling Fee 200.00"
    result = extract_invoice_fields(text)

    assert result["invoice_number"] == "INV-2026-001"
    assert str(result["total_amount"]) == "1400.50"
    assert len(result["line_items"]) >= 2


def test_extract_invoice_document_supports_utf8_upload() -> None:
    result = extract_invoice_document("invoice.txt", b"Invoice Number: INV-1\nDelivery Lagos-Abuja 500.00")

    assert result["invoice_number"] == "INV-1"
    assert result["extraction_method"] == "utf8_text"
