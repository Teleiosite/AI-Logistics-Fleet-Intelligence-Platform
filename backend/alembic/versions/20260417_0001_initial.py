"""initial schema

Revision ID: 20260417_0001
Revises:
Create Date: 2026-04-17
"""

from alembic import op
import sqlalchemy as sa


revision = "20260417_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False, unique=True),
        sa.Column("timezone", sa.String(length=50), nullable=False),
        sa.Column("subscription_tier", sa.String(length=50), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("company_id", sa.String(length=36), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("role", sa.String(length=100), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
    )

    op.create_table(
        "vehicles",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("company_id", sa.String(length=36), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("vehicle_number", sa.String(length=50), nullable=False),
        sa.Column("license_plate", sa.String(length=20), nullable=False, unique=True),
        sa.Column("vehicle_type", sa.String(length=50), nullable=False),
        sa.Column("tank_capacity_liters", sa.Numeric(10, 2), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("vehicles")
    op.drop_table("users")
    op.drop_table("companies")
