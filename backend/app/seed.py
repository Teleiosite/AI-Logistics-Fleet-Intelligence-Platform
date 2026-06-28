"""Demo seed script – populates the database with a sample company, users, fleet,
shipments, fuel logs, and invoices so the platform can be demoed out of the box.

Usage:
    python app/seed.py

The script is idempotent: running it twice will not create duplicate records.
"""

import sys
import time
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

# Allow running directly with `python app/seed.py` from the backend directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select

from app.core.config import get_settings
from app.core.security import hash_password
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.entities import (
    Alert,
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

settings = get_settings()

DEMO_COMPANY_SLUG = "acme-logistics"
DEMO_USER_EMAIL = "admin@acme-logistics.demo"
DEMO_PASSWORD = "FleetIQ2026!"


def wait_for_db(max_retries: int = 20, delay: float = 2.0) -> None:
    """Wait for the database to be ready before seeding."""
    from sqlalchemy import text

    for attempt in range(1, max_retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except Exception as exc:
            if attempt == max_retries:
                raise RuntimeError("Database not available after retries") from exc
            print(f"[seed] DB not ready (attempt {attempt}/{max_retries}), retrying in {delay}s…")
            time.sleep(delay)


def seed() -> None:
    # Ensure tables exist (create_all is a no-op when tables already exist)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # -- Company -------------------------------------------------------
        company = db.scalar(select(Company).where(Company.slug == DEMO_COMPANY_SLUG))
        if not company:
            company = Company(
                name="ACME Logistics Ltd",
                slug=DEMO_COMPANY_SLUG,
                timezone="Africa/Lagos",
                subscription_tier="enterprise",
            )
            db.add(company)
            db.flush()
            print(f"[seed] Created company: {company.name} (id={company.id})")
        else:
            print(f"[seed] Company already exists: {company.name}")

        # -- Admin user ----------------------------------------------------
        admin = db.scalar(select(User).where(User.email == DEMO_USER_EMAIL))
        if not admin:
            admin = User(
                company_id=company.id,
                email=DEMO_USER_EMAIL,
                password_hash=hash_password(DEMO_PASSWORD),
                first_name="Admin",
                last_name="Demo",
                role="company_admin",
            )
            db.add(admin)
            db.flush()
            print(f"[seed] Created admin user: {DEMO_USER_EMAIL}")
        else:
            print(f"[seed] Admin user already exists: {DEMO_USER_EMAIL}")

        # -- Vehicles ------------------------------------------------------
        vehicles = []
        vehicle_specs = [
            ("VH-001", "LAG-001-AA", "truck", Decimal("600")),
            ("VH-002", "LAG-002-BB", "truck", Decimal("500")),
            ("VH-003", "ABJ-003-CC", "van", Decimal("80")),
        ]
        for vnum, plate, vtype, capacity in vehicle_specs:
            v = db.scalar(select(Vehicle).where(Vehicle.license_plate == plate))
            if not v:
                v = Vehicle(
                    company_id=company.id,
                    vehicle_number=vnum,
                    license_plate=plate,
                    vehicle_type=vtype,
                    tank_capacity_liters=capacity,
                    status="active",
                )
                db.add(v)
                db.flush()
                print(f"[seed] Created vehicle: {plate}")
            vehicles.append(v)

        # -- Drivers -------------------------------------------------------
        drivers = []
        driver_specs = [
            ("Emeka", "Okafor", "+2348031234567", "DRV-LG-001"),
            ("Bola", "Adeleke", "+2348039876543", "DRV-LG-002"),
            ("Chidi", "Nwachukwu", "+2348055551234", "DRV-AB-001"),
        ]
        for fn, ln, phone, lic in driver_specs:
            d = db.scalar(select(Driver).where(Driver.license_number == lic))
            if not d:
                d = Driver(
                    company_id=company.id,
                    first_name=fn,
                    last_name=ln,
                    phone=phone,
                    license_number=lic,
                    status="active",
                )
                db.add(d)
                db.flush()
                print(f"[seed] Created driver: {fn} {ln}")
            drivers.append(d)

        # -- Transporter ---------------------------------------------------
        transporter = db.scalar(
            select(Transporter).where(
                Transporter.company_id == company.id,
                Transporter.name == "Swift Haulage Co",
            )
        )
        if not transporter:
            transporter = Transporter(
                company_id=company.id,
                name="Swift Haulage Co",
                contact_person="James Adeyemi",
                phone="+2348012345678",
                email="ops@swifthaulage.example",
                performance_score=Decimal("4.20"),
                status="active",
            )
            db.add(transporter)
            db.flush()
            print(f"[seed] Created transporter: Swift Haulage Co")

        # -- Shipments -----------------------------------------------------
        shipment_specs = [
            ("SHP-2026-001", "Dangote Industries", "5 Commercial Rd, Apapa, Lagos", "Plot 45 Industrial Layout, Kano", ShipmentStatus.DELIVERED, vehicles[0], drivers[0]),
            ("SHP-2026-002", "MTN Nigeria", "22 Marina St, Lagos Island", "Central Business District, Abuja", ShipmentStatus.IN_TRANSIT, vehicles[1], drivers[1]),
            ("SHP-2026-003", "Flour Mills Nigeria", "Tin Can Island Port, Lagos", "Eastern Bypass, Enugu", ShipmentStatus.DELAYED, vehicles[0], drivers[0]),
            ("SHP-2026-004", "Nestle Nigeria", "Agbara Industrial Estate, Ogun", "Ring Road, Ibadan", ShipmentStatus.ASSIGNED, vehicles[2], drivers[2]),
            ("SHP-2026-005", "PZ Cussons", "Victoria Island, Lagos", "Trans-Amadi Estate, Port Harcourt", ShipmentStatus.DRAFT, None, None),
        ]
        shipments = []
        for snum, cust, pickup, delivery, status, vehicle, driver in shipment_specs:
            s = db.scalar(select(Shipment).where(Shipment.shipment_number == snum))
            if not s:
                now = datetime.utcnow()
                s = Shipment(
                    company_id=company.id,
                    shipment_number=snum,
                    customer_name=cust,
                    pickup_address=pickup,
                    delivery_address=delivery,
                    vehicle_id=vehicle.id if vehicle else None,
                    driver_id=driver.id if driver else None,
                    status=status,
                    proof_of_delivery_url="https://example.com/pod/sample.jpg" if status == ShipmentStatus.DELIVERED else None,
                    created_at=now - timedelta(days=len(shipments) + 1),
                    updated_at=now,
                )
                db.add(s)
                db.flush()
                log = ShipmentStatusLog(
                    shipment_id=s.id,
                    from_status=None,
                    to_status=status.value,
                    notes="Seeded",
                    created_at=s.created_at,
                )
                db.add(log)
                db.flush()
                print(f"[seed] Created shipment: {snum} ({status.value})")
            shipments.append(s)

        # -- Fuel logs -----------------------------------------------------
        fuel_specs = [
            (vehicles[0], shipments[0], Decimal("350"), Decimal("650"), None),
            (vehicles[1], shipments[1], Decimal("280"), Decimal("650"), None),
            (vehicles[0], shipments[2], Decimal("720"), Decimal("650"), None),   # anomaly: >110% capacity
        ]
        for veh, ship, qty, price, odo in fuel_specs:
            existing = db.scalar(
                select(FuelIssuanceLog).where(
                    FuelIssuanceLog.company_id == company.id,
                    FuelIssuanceLog.vehicle_id == veh.id,
                    FuelIssuanceLog.shipment_id == ship.id,
                )
            )
            if not existing:
                total = (qty * price).quantize(Decimal("0.01"))
                is_anomaly = False
                anomaly_reason = None
                if veh.tank_capacity_liters and qty > veh.tank_capacity_liters * Decimal("1.10"):
                    is_anomaly = True
                    anomaly_reason = "Excessive fill: exceeds 110% of tank capacity"
                log = FuelIssuanceLog(
                    company_id=company.id,
                    vehicle_id=veh.id,
                    shipment_id=ship.id,
                    quantity_liters=qty,
                    price_per_liter=price,
                    total_cost=total,
                    odometer_reading_km=odo,
                    is_anomaly=is_anomaly,
                    anomaly_reason=anomaly_reason,
                    created_at=datetime.utcnow() - timedelta(hours=len(fuel_specs)),
                )
                db.add(log)
                db.flush()
                print(f"[seed] Created fuel log: vehicle={veh.vehicle_number} qty={qty}L anomaly={is_anomaly}")

        # -- Invoice -------------------------------------------------------
        invoice = db.scalar(
            select(Invoice).where(
                Invoice.company_id == company.id,
                Invoice.invoice_number == "INV-2026-SWFT-001",
            )
        )
        if not invoice:
            invoice = Invoice(
                company_id=company.id,
                transporter_id=transporter.id,
                invoice_number="INV-2026-SWFT-001",
                total_amount=Decimal("485000.00"),
                discrepancy_count=1,
                status="pending",
                created_at=datetime.utcnow() - timedelta(days=3),
            )
            db.add(invoice)
            db.flush()
            # Line items
            line_items = [
                InvoiceLineItem(
                    invoice_id=invoice.id,
                    shipment_id=shipments[0].id,
                    description="Lagos-Kano route: SHP-2026-001",
                    amount=Decimal("285000.00"),
                    is_matched=True,
                    has_discrepancy=False,
                ),
                InvoiceLineItem(
                    invoice_id=invoice.id,
                    shipment_id=None,
                    description="Unmatched fuel surcharge",
                    amount=Decimal("200000.00"),
                    is_matched=False,
                    has_discrepancy=True,
                ),
            ]
            for item in line_items:
                db.add(item)
            db.flush()
            print(f"[seed] Created invoice: INV-2026-SWFT-001")

        # -- DVR -----------------------------------------------------------
        dvr = db.scalar(
            select(DeliveryVarianceReport).where(
                DeliveryVarianceReport.dvr_number == "DVR-2026-001"
            )
        )
        if not dvr:
            dvr = DeliveryVarianceReport(
                company_id=company.id,
                shipment_id=shipments[2].id,
                dvr_number="DVR-2026-001",
                variance_type="quantity_shortage",
                description="Customer reports 50kg short delivery on cement order.",
                financial_impact=Decimal("15000.00"),
                status="open",
                created_at=datetime.utcnow() - timedelta(days=1),
            )
            db.add(dvr)
            db.flush()
            print(f"[seed] Created DVR: DVR-2026-001")

        # -- Alert ---------------------------------------------------------
        alert = db.scalar(
            select(Alert).where(Alert.company_id == company.id, Alert.alert_type == "fuel_anomaly")
        )
        if not alert:
            alert = Alert(
                company_id=company.id,
                alert_type="fuel_anomaly",
                severity="critical",
                title="Excessive fuel fill detected",
                message="Vehicle VH-003 received 720L which exceeds tank capacity of 600L by >10%.",
                status="active",
                created_at=datetime.utcnow(),
            )
            db.add(alert)
            db.flush()
            print(f"[seed] Created alert: fuel_anomaly")

        db.commit()
        print("\n✅ Seed completed successfully!")
        print(f"\n🔑 Demo login credentials:")
        print(f"   Email   : {DEMO_USER_EMAIL}")
        print(f"   Password: {DEMO_PASSWORD}")
        print(f"\n📌 Company ID: {company.id}")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    wait_for_db()
    seed()
