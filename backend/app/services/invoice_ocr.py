import re
from decimal import Decimal


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
