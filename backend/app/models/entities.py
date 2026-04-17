from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ShipmentStatus(StrEnum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ASSIGNED = "assigned"
    DISPATCHED = "dispatched"
    EN_ROUTE_TO_PICKUP = "en_route_to_pickup"
    AT_PICKUP = "at_pickup"
    LOADED = "loaded"
    IN_TRANSIT = "in_transit"
    AT_DELIVERY = "at_delivery"
    UNLOADING = "unloading"
    DELIVERED = "delivered"
    DELAYED = "delayed"
    EXCEPTION = "exception"


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), default="Africa/Lagos")
    subscription_tier: Mapped[str] = mapped_column(String(50), default="starter")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    users: Mapped[list["User"]] = relationship(back_populates="company")


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    company_id: Mapped[str] = mapped_column(String(36), ForeignKey("companies.id"), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(100), default="company_admin")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    company: Mapped[Company] = relationship(back_populates="users")


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    company_id: Mapped[str] = mapped_column(String(36), ForeignKey("companies.id"), nullable=False)
    vehicle_number: Mapped[str] = mapped_column(String(50), nullable=False)
    license_plate: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    vehicle_type: Mapped[str] = mapped_column(String(50), default="truck")
    tank_capacity_liters: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active")


class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    company_id: Mapped[str] = mapped_column(String(36), ForeignKey("companies.id"), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    license_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active")


class Transporter(Base):
    __tablename__ = "transporters"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    company_id: Mapped[str] = mapped_column(String(36), ForeignKey("companies.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_person: Mapped[str | None] = mapped_column(String(200), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    performance_score: Mapped[Decimal] = mapped_column(Numeric(3, 2), default=Decimal("5.00"))
    status: Mapped[str] = mapped_column(String(50), default="active")


class Shipment(Base):
    __tablename__ = "shipments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    company_id: Mapped[str] = mapped_column(String(36), ForeignKey("companies.id"), nullable=False)
    shipment_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    pickup_address: Mapped[str] = mapped_column(Text, nullable=False)
    delivery_address: Mapped[str] = mapped_column(Text, nullable=False)
    vehicle_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("vehicles.id"), nullable=True)
    driver_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("drivers.id"), nullable=True)
    transporter_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("transporters.id"), nullable=True)
    status: Mapped[ShipmentStatus] = mapped_column(Enum(ShipmentStatus), default=ShipmentStatus.DRAFT)
    proof_of_delivery_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    delivery_signature_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    has_variance: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ShipmentStatusLog(Base):
    __tablename__ = "shipment_status_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    shipment_id: Mapped[str] = mapped_column(String(36), ForeignKey("shipments.id"), nullable=False)
    from_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    to_status: Mapped[str] = mapped_column(String(50), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class FuelIssuanceLog(Base):
    __tablename__ = "fuel_issuance_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    company_id: Mapped[str] = mapped_column(String(36), ForeignKey("companies.id"), nullable=False)
    vehicle_id: Mapped[str] = mapped_column(String(36), ForeignKey("vehicles.id"), nullable=False)
    shipment_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("shipments.id"), nullable=True)
    quantity_liters: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    price_per_liter: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    total_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    odometer_reading_km: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    is_anomaly: Mapped[bool] = mapped_column(Boolean, default=False)
    anomaly_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class DeliveryVarianceReport(Base):
    __tablename__ = "delivery_variance_reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    company_id: Mapped[str] = mapped_column(String(36), ForeignKey("companies.id"), nullable=False)
    shipment_id: Mapped[str] = mapped_column(String(36), ForeignKey("shipments.id"), nullable=False)
    dvr_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    variance_type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    financial_impact: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="open")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    company_id: Mapped[str] = mapped_column(String(36), ForeignKey("companies.id"), nullable=False)
    transporter_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("transporters.id"), nullable=True)
    invoice_number: Mapped[str] = mapped_column(String(100), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    discrepancy_count: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class InvoiceLineItem(Base):
    __tablename__ = "invoice_line_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    invoice_id: Mapped[str] = mapped_column(String(36), ForeignKey("invoices.id"), nullable=False)
    shipment_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("shipments.id"), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    is_matched: Mapped[bool] = mapped_column(Boolean, default=False)
    has_discrepancy: Mapped[bool] = mapped_column(Boolean, default=False)


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    company_id: Mapped[str] = mapped_column(String(36), ForeignKey("companies.id"), nullable=False)
    alert_type: Mapped[str] = mapped_column(String(50), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default="warning")
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
