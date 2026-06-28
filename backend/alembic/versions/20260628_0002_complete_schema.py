"""complete schema – add all domain tables

Revision ID: 20260628_0002
Revises: 20260417_0001
Create Date: 2026-06-28
"""

from alembic import op
import sqlalchemy as sa

revision = "20260628_0002"
down_revision = "20260417_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "drivers",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("company_id", sa.String(length=36), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=False),
        sa.Column("license_number", sa.String(length=50), nullable=False, unique=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="active"),
    )

    op.create_table(
        "transporters",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("company_id", sa.String(length=36), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("contact_person", sa.String(length=200), nullable=True),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("performance_score", sa.Numeric(3, 2), nullable=False, server_default="5.00"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="active"),
    )

    op.create_table(
        "shipments",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("company_id", sa.String(length=36), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("shipment_number", sa.String(length=50), nullable=False, unique=True),
        sa.Column("customer_name", sa.String(length=255), nullable=False),
        sa.Column("pickup_address", sa.Text(), nullable=False),
        sa.Column("delivery_address", sa.Text(), nullable=False),
        sa.Column("vehicle_id", sa.String(length=36), sa.ForeignKey("vehicles.id"), nullable=True),
        sa.Column("driver_id", sa.String(length=36), sa.ForeignKey("drivers.id"), nullable=True),
        sa.Column("transporter_id", sa.String(length=36), sa.ForeignKey("transporters.id"), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "draft", "scheduled", "assigned", "dispatched",
                "en_route_to_pickup", "at_pickup", "loaded", "in_transit",
                "at_delivery", "unloading", "delivered", "delayed", "exception",
                name="shipmentstatus",
            ),
            nullable=False,
            server_default="draft",
        ),
        sa.Column("proof_of_delivery_url", sa.Text(), nullable=True),
        sa.Column("delivery_signature_url", sa.Text(), nullable=True),
        sa.Column("has_variance", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "shipment_status_logs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("shipment_id", sa.String(length=36), sa.ForeignKey("shipments.id"), nullable=False),
        sa.Column("from_status", sa.String(length=50), nullable=True),
        sa.Column("to_status", sa.String(length=50), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "fuel_issuance_logs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("company_id", sa.String(length=36), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("vehicle_id", sa.String(length=36), sa.ForeignKey("vehicles.id"), nullable=False),
        sa.Column("shipment_id", sa.String(length=36), sa.ForeignKey("shipments.id"), nullable=True),
        sa.Column("quantity_liters", sa.Numeric(10, 2), nullable=False),
        sa.Column("price_per_liter", sa.Numeric(10, 2), nullable=False),
        sa.Column("total_cost", sa.Numeric(12, 2), nullable=False),
        sa.Column("odometer_reading_km", sa.Numeric(10, 2), nullable=True),
        sa.Column("is_anomaly", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("anomaly_reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "delivery_variance_reports",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("company_id", sa.String(length=36), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("shipment_id", sa.String(length=36), sa.ForeignKey("shipments.id"), nullable=False),
        sa.Column("dvr_number", sa.String(length=50), nullable=False, unique=True),
        sa.Column("variance_type", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("financial_impact", sa.Numeric(12, 2), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="open"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "invoices",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("company_id", sa.String(length=36), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("transporter_id", sa.String(length=36), sa.ForeignKey("transporters.id"), nullable=True),
        sa.Column("invoice_number", sa.String(length=100), nullable=False),
        sa.Column("total_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("discrepancy_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "invoice_line_items",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("invoice_id", sa.String(length=36), sa.ForeignKey("invoices.id"), nullable=False),
        sa.Column("shipment_id", sa.String(length=36), sa.ForeignKey("shipments.id"), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("is_matched", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("has_discrepancy", sa.Boolean(), nullable=False, server_default=sa.false()),
    )

    op.create_table(
        "alerts",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("company_id", sa.String(length=36), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("alert_type", sa.String(length=50), nullable=False),
        sa.Column("severity", sa.String(length=50), nullable=False, server_default="warning"),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("alerts")
    op.drop_table("invoice_line_items")
    op.drop_table("invoices")
    op.drop_table("delivery_variance_reports")
    op.drop_table("fuel_issuance_logs")
    op.drop_table("shipment_status_logs")
    op.drop_table("shipments")
    op.drop_table("transporters")
    op.drop_table("drivers")
    # Drop the enum type created for shipment status
    op.execute("DROP TYPE IF EXISTS shipmentstatus")
