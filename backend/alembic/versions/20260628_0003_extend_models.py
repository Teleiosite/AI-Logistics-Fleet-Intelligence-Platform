"""extend models with shipment, fuel, and audit fields

Revision ID: 20260628_0003
Revises: 20260628_0002
Create Date: 2026-06-28
"""

from alembic import op
import sqlalchemy as sa

revision = "20260628_0003"
down_revision = "20260628_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("shipments", sa.Column("priority", sa.String(length=50), server_default="standard", nullable=False))
    op.add_column("shipments", sa.Column("scheduled_pickup_at", sa.DateTime(), nullable=True))
    op.add_column("shipments", sa.Column("scheduled_delivery_at", sa.DateTime(), nullable=True))
    op.add_column("shipments", sa.Column("cargo_description", sa.Text(), nullable=True))
    op.add_column("shipments", sa.Column("cargo_weight_kg", sa.Numeric(10, 2), nullable=True))
    op.add_column("shipments", sa.Column("cargo_volume_m3", sa.Numeric(10, 2), nullable=True))
    op.add_column("shipments", sa.Column("reference_number", sa.String(length=100), nullable=True))
    op.add_column("fuel_issuance_logs", sa.Column("fuel_efficiency_lkm", sa.Numeric(8, 3), nullable=True))
    op.add_column("fuel_issuance_logs", sa.Column("station_name", sa.String(length=200), nullable=True))
    op.add_column("delivery_variance_reports", sa.Column("fault_assignment", sa.String(length=50), nullable=True))
    op.add_column("delivery_variance_reports", sa.Column("severity", sa.String(length=50), server_default="minor", nullable=False))
    op.add_column("delivery_variance_reports", sa.Column("resolution_notes", sa.Text(), nullable=True))
    op.add_column("delivery_variance_reports", sa.Column("updated_at", sa.DateTime(), nullable=True))

    op.create_table(
        "fuel_price_history",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("company_id", sa.String(length=36), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("region", sa.String(length=100), nullable=False),
        sa.Column("fuel_type", sa.String(length=50), nullable=False, server_default="diesel"),
        sa.Column("price_per_liter", sa.Numeric(10, 2), nullable=False),
        sa.Column("recorded_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("company_id", sa.String(length=36), nullable=True),
        sa.Column("user_email", sa.String(length=255), nullable=False),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("resource", sa.String(length=100), nullable=False),
        sa.Column("resource_id", sa.String(length=36), nullable=True),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("fuel_price_history")
    op.drop_column("delivery_variance_reports", "updated_at")
    op.drop_column("delivery_variance_reports", "resolution_notes")
    op.drop_column("delivery_variance_reports", "severity")
    op.drop_column("delivery_variance_reports", "fault_assignment")
    op.drop_column("fuel_issuance_logs", "station_name")
    op.drop_column("fuel_issuance_logs", "fuel_efficiency_lkm")
    op.drop_column("shipments", "reference_number")
    op.drop_column("shipments", "cargo_volume_m3")
    op.drop_column("shipments", "cargo_weight_kg")
    op.drop_column("shipments", "cargo_description")
    op.drop_column("shipments", "scheduled_delivery_at")
    op.drop_column("shipments", "scheduled_pickup_at")
    op.drop_column("shipments", "priority")
