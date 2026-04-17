from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.entities import (
    Company,
    DeliveryVarianceReport,
    Driver,
    FuelIssuanceLog,
    Invoice,
    InvoiceLineItem,
    Shipment,
    ShipmentStatus,
    ShipmentStatusLog,
    Transporter,
    User,
    Vehicle,
)
from app.schemas.auth import RegisterRequest
from app.schemas.company import CompanyCreate
from app.schemas.dvr import DVRCreate
from app.schemas.fleet import DriverCreate, TransporterCreate, VehicleCreate
from app.schemas.fuel import FuelLogCreate
from app.schemas.invoice import InvoiceCreate, InvoiceUploadText
from app.schemas.shipment import ShipmentCreate
from app.services.invoice_ocr import extract_invoice_fields


# Companies

def create_company(db: Session, payload: CompanyCreate) -> Company:
    entity = Company(**payload.model_dump())
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def list_companies(db: Session) -> list[Company]:
    return list(db.scalars(select(Company).order_by(Company.created_at.desc())))


# Auth / Users

def create_user(db: Session, payload: RegisterRequest, password_hash: str) -> User:
    entity = User(
        company_id=payload.company_id,
        email=payload.email,
        password_hash=password_hash,
        first_name=payload.first_name,
        last_name=payload.last_name,
        role=payload.role,
    )
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email))


# Fleet

def create_vehicle(db: Session, company_id: str, payload: VehicleCreate) -> Vehicle:
    entity = Vehicle(company_id=company_id, **payload.model_dump())
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def list_vehicles(db: Session, company_id: str) -> list[Vehicle]:
    return list(db.scalars(select(Vehicle).where(Vehicle.company_id == company_id)))


def create_driver(db: Session, company_id: str, payload: DriverCreate) -> Driver:
    entity = Driver(company_id=company_id, **payload.model_dump())
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def list_drivers(db: Session, company_id: str) -> list[Driver]:
    return list(db.scalars(select(Driver).where(Driver.company_id == company_id)))


def create_transporter(db: Session, company_id: str, payload: TransporterCreate) -> Transporter:
    entity = Transporter(company_id=company_id, **payload.model_dump())
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def list_transporters(db: Session, company_id: str) -> list[Transporter]:
    return list(db.scalars(select(Transporter).where(Transporter.company_id == company_id)))


# Shipments

def create_shipment(db: Session, company_id: str, payload: ShipmentCreate) -> Shipment:
    entity = Shipment(company_id=company_id, **payload.model_dump())
    db.add(entity)
    db.flush()

    log = ShipmentStatusLog(shipment_id=entity.id, from_status=None, to_status=ShipmentStatus.DRAFT.value, notes="Shipment created")
    db.add(log)
    db.commit()
    db.refresh(entity)
    return entity


def list_shipments(db: Session, company_id: str) -> list[Shipment]:
    stmt = select(Shipment).where(Shipment.company_id == company_id).order_by(Shipment.created_at.desc())
    return list(db.scalars(stmt))


# Fuel

def create_fuel_log(db: Session, company_id: str, payload: FuelLogCreate) -> FuelIssuanceLog:
    total_cost = (payload.quantity_liters * payload.price_per_liter).quantize(Decimal("0.01"))
    entity = FuelIssuanceLog(company_id=company_id, **payload.model_dump(), total_cost=total_cost)

    vehicle = db.get(Vehicle, payload.vehicle_id)
    if vehicle and vehicle.tank_capacity_liters and payload.quantity_liters > vehicle.tank_capacity_liters * Decimal("1.10"):
        entity.is_anomaly = True
        entity.anomaly_reason = "Excessive fill: exceeds 110% of tank capacity"

    since = datetime.utcnow() - timedelta(hours=24)
    recent_count = (
        db.scalar(
            select(func.count(FuelIssuanceLog.id)).where(
                FuelIssuanceLog.company_id == company_id,
                FuelIssuanceLog.vehicle_id == payload.vehicle_id,
                FuelIssuanceLog.created_at >= since,
            )
        )
        or 0
    )
    if recent_count >= 2:
        entity.is_anomaly = True
        entity.anomaly_reason = "Frequency anomaly: more than 2 fills in 24 hours"

    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def list_fuel_logs(db: Session, company_id: str) -> list[FuelIssuanceLog]:
    return list(db.scalars(select(FuelIssuanceLog).where(FuelIssuanceLog.company_id == company_id)))


# DVR

def create_dvr(db: Session, company_id: str, payload: DVRCreate) -> DeliveryVarianceReport:
    entity = DeliveryVarianceReport(company_id=company_id, **payload.model_dump())
    shipment = db.get(Shipment, payload.shipment_id)
    if shipment and shipment.company_id == company_id:
        shipment.has_variance = True
        db.add(shipment)
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def list_dvrs(db: Session, company_id: str) -> list[DeliveryVarianceReport]:
    return list(db.scalars(select(DeliveryVarianceReport).where(DeliveryVarianceReport.company_id == company_id)))


# Invoices

def create_invoice(db: Session, company_id: str, payload: InvoiceCreate) -> Invoice:
    entity = Invoice(company_id=company_id, **payload.model_dump())
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def create_invoice_from_text(db: Session, company_id: str, payload: InvoiceUploadText) -> Invoice:
    extracted = extract_invoice_fields(payload.raw_text)
    invoice = Invoice(
        company_id=company_id,
        transporter_id=payload.transporter_id,
        invoice_number=str(extracted["invoice_number"]),
        total_amount=Decimal(str(extracted["total_amount"])),
    )
    db.add(invoice)
    db.flush()

    for row in extracted["line_items"]:
        item = InvoiceLineItem(
            invoice_id=invoice.id,
            description=str(row["description"]),
            amount=Decimal(str(row["amount"])),
        )
        db.add(item)

    db.commit()
    db.refresh(invoice)
    return invoice


def list_invoices(db: Session, company_id: str) -> list[Invoice]:
    return list(db.scalars(select(Invoice).where(Invoice.company_id == company_id)))


def auto_match_invoice(db: Session, company_id: str, invoice_id: str) -> dict[str, int]:
    invoice = db.scalar(select(Invoice).where(Invoice.id == invoice_id, Invoice.company_id == company_id))
    if not invoice:
        return {"matched": 0, "discrepancies": 0}

    items = list(db.scalars(select(InvoiceLineItem).where(InvoiceLineItem.invoice_id == invoice_id)))
    matched = 0
    discrepancies = 0

    for item in items:
        if not item.shipment_id:
            item.has_discrepancy = True
            discrepancies += 1
            db.add(item)
            continue
        shipment = db.get(Shipment, item.shipment_id)
        if shipment and shipment.company_id == company_id:
            item.is_matched = True
            matched += 1
        else:
            item.has_discrepancy = True
            discrepancies += 1
        db.add(item)

    invoice.discrepancy_count = discrepancies
    db.add(invoice)
    db.commit()
    return {"matched": matched, "discrepancies": discrepancies}


def generate_dispute_memo(db: Session, company_id: str, invoice_id: str) -> str:
    invoice = db.scalar(select(Invoice).where(Invoice.id == invoice_id, Invoice.company_id == company_id))
    if not invoice:
        return "Invoice not found"

    items = list(db.scalars(select(InvoiceLineItem).where(InvoiceLineItem.invoice_id == invoice_id)))
    disputed = [item for item in items if item.has_discrepancy]
    lines = [
        f"Dispute Memo - Invoice {invoice.invoice_number}",
        f"Company: {company_id}",
        f"Discrepancy count: {invoice.discrepancy_count}",
        "",
    ]
    for idx, item in enumerate(disputed, start=1):
        lines.append(f"{idx}. Line item {item.id}: amount={item.amount}, shipment_id={item.shipment_id}")

    if not disputed:
        lines.append("No discrepancies detected.")

    return "\n".join(lines)


# Analytics

def get_shipment_metrics(db: Session, company_id: str) -> dict[str, int]:
    total = db.scalar(select(func.count(Shipment.id)).where(Shipment.company_id == company_id)) or 0
    delayed = (
        db.scalar(
            select(func.count(Shipment.id)).where(
                Shipment.company_id == company_id,
                Shipment.status == ShipmentStatus.DELAYED,
            )
        )
        or 0
    )
    delivered = (
        db.scalar(
            select(func.count(Shipment.id)).where(
                Shipment.company_id == company_id,
                Shipment.status == ShipmentStatus.DELIVERED,
            )
        )
        or 0
    )
    active = total - delivered
    return {
        "total_shipments": int(total),
        "active_shipments": int(active),
        "delayed_shipments": int(delayed),
        "delivered_shipments": int(delivered),
    }
