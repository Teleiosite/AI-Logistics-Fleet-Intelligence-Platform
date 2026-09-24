from datetime import datetime, timedelta
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import func, select, update as sa_update
from sqlalchemy.orm import Session

from app.models.entities import (
    Company,
    DeliveryVarianceReport,
    Driver,
    FuelIssuanceLog,
    FuelPriceHistory,
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

if TYPE_CHECKING:
    from app.schemas.fuel_price import FuelPriceCreate


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


def list_users(db: Session, company_id: str) -> list[User]:
    return list(db.scalars(select(User).where(User.company_id == company_id, User.is_active == True)))


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

    if payload.odometer_reading_km is not None:
        previous_log = db.scalar(
            select(FuelIssuanceLog)
            .where(
                FuelIssuanceLog.company_id == company_id,
                FuelIssuanceLog.vehicle_id == payload.vehicle_id,
                FuelIssuanceLog.odometer_reading_km.is_not(None),
            )
            .order_by(FuelIssuanceLog.created_at.desc())
        )
        if previous_log and payload.odometer_reading_km > previous_log.odometer_reading_km:
            distance = payload.odometer_reading_km - previous_log.odometer_reading_km
            entity.fuel_efficiency_lkm = (payload.quantity_liters / distance * Decimal("100")).quantize(Decimal("0.001"))

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


def create_fuel_price(db: Session, company_id: str, payload: "FuelPriceCreate") -> FuelPriceHistory:
    entity = FuelPriceHistory(company_id=company_id, **payload.model_dump())
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def list_fuel_prices(db: Session, company_id: str) -> list[FuelPriceHistory]:
    return list(
        db.scalars(
            select(FuelPriceHistory)
            .where(FuelPriceHistory.company_id == company_id)
            .order_by(FuelPriceHistory.recorded_at.desc())
        )
    )


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


def update_dvr_status(
    db: Session,
    company_id: str,
    dvr_id: str,
    status: str,
    resolution_notes: str | None = None,
    fault_assignment: str | None = None,
) -> DeliveryVarianceReport | None:
    dvr = db.scalar(
        select(DeliveryVarianceReport).where(
            DeliveryVarianceReport.id == dvr_id,
            DeliveryVarianceReport.company_id == company_id,
        )
    )
    if not dvr:
        return None
    dvr.status = status
    if resolution_notes is not None:
        dvr.resolution_notes = resolution_notes
    if fault_assignment is not None:
        dvr.fault_assignment = fault_assignment
    db.add(dvr)
    db.commit()
    db.refresh(dvr)
    return dvr


def recalculate_transporter_score(db: Session, transporter_id: str) -> None:
    total = (
        db.scalar(
            select(func.count(Shipment.id)).where(
                Shipment.transporter_id == transporter_id,
                Shipment.status == ShipmentStatus.DELIVERED,
            )
        )
        or 0
    )
    if total == 0:
        return
    on_time = (
        db.scalar(
            select(func.count(Shipment.id)).where(
                Shipment.transporter_id == transporter_id,
                Shipment.status == ShipmentStatus.DELIVERED,
                ~Shipment.has_variance,
            )
        )
        or 0
    )
    rate = on_time / total
    score = round(min(Decimal("10.00"), max(Decimal("1.00"), Decimal(str(rate * 10)))), 2)
    db.execute(sa_update(Transporter).where(Transporter.id == transporter_id).values(performance_score=score))
    db.commit()


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


def get_fuel_metrics(db: Session, company_id: str) -> dict:
    logs = list_fuel_logs(db, company_id)
    total_volume = sum(float(log.quantity_liters) for log in logs)
    total_cost = sum(float(log.total_cost) for log in logs)
    anomaly_count = sum(1 for log in logs if log.is_anomaly)
    efficiencies = [float(log.fuel_efficiency_lkm) for log in logs if log.fuel_efficiency_lkm]
    avg_efficiency = round(sum(efficiencies) / len(efficiencies), 3) if efficiencies else None
    return {
        "total_volume_liters": round(total_volume, 2),
        "total_cost": round(total_cost, 2),
        "anomaly_count": anomaly_count,
        "avg_efficiency_lkm": avg_efficiency,
    }


def get_fleet_metrics(db: Session, company_id: str) -> dict:
    vehicles = list_vehicles(db, company_id)
    drivers = list_drivers(db, company_id)
    active_vehicles = sum(1 for vehicle in vehicles if vehicle.status == "active")
    maintenance_vehicles = sum(1 for vehicle in vehicles if vehicle.status == "maintenance")
    active_drivers = sum(1 for driver in drivers if driver.status == "active")
    return {
        "total_vehicles": len(vehicles),
        "active_vehicles": active_vehicles,
        "maintenance_vehicles": maintenance_vehicles,
        "total_drivers": len(drivers),
        "active_drivers": active_drivers,
    }


def get_dvr_metrics(db: Session, company_id: str) -> dict:
    dvrs = list_dvrs(db, company_id)
    open_count = sum(1 for dvr in dvrs if dvr.status == "open")
    resolved_count = sum(1 for dvr in dvrs if dvr.status in ("resolved", "closed"))
    by_type: dict[str, int] = {}
    for dvr in dvrs:
        by_type[dvr.variance_type] = by_type.get(dvr.variance_type, 0) + 1
    return {
        "total": len(dvrs),
        "open": open_count,
        "resolved": resolved_count,
        "by_type": [{"type": key, "count": value} for key, value in by_type.items()],
    }


def get_shipment_trend(db: Session, company_id: str, days: int = 7) -> list[dict]:
    result = []
    today = datetime.utcnow().date()
    for i in range(days - 1, -1, -1):
        day = today - timedelta(days=i)
        start = datetime(day.year, day.month, day.day)
        end = start + timedelta(days=1)
        count = (
            db.scalar(
                select(func.count(Shipment.id)).where(
                    Shipment.company_id == company_id,
                    Shipment.created_at >= start,
                    Shipment.created_at < end,
                )
            )
            or 0
        )
        result.append({"date": day.isoformat(), "count": count})
    return result
