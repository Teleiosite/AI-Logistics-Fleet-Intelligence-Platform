from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect

from app.core.config import get_settings

BACKEND_DIR = Path(__file__).resolve().parents[1]
EXPECTED_TABLES = {
    "alerts",
    "alembic_version",
    "audit_logs",
    "companies",
    "delivery_variance_reports",
    "drivers",
    "fuel_issuance_logs",
    "fuel_price_history",
    "invoice_line_items",
    "invoices",
    "shipment_status_logs",
    "shipments",
    "transporters",
    "users",
    "vehicles",
}


def test_alembic_upgrade_creates_full_schema(tmp_path, monkeypatch) -> None:
    db_url = f"sqlite+pysqlite:///{tmp_path / 'migrations.db'}"
    monkeypatch.setenv("DATABASE_URL", db_url)
    get_settings.cache_clear()

    config = Config(str(BACKEND_DIR / "alembic.ini"))
    config.set_main_option("script_location", str(BACKEND_DIR / "alembic"))
    config.set_main_option("sqlalchemy.url", db_url)

    command.upgrade(config, "head")

    engine = create_engine(db_url)
    try:
        inspector = inspect(engine)
        assert EXPECTED_TABLES.issubset(set(inspector.get_table_names()))

        shipment_columns = {column["name"] for column in inspector.get_columns("shipments")}
        assert {
            "priority",
            "scheduled_pickup_at",
            "scheduled_delivery_at",
            "cargo_description",
            "cargo_weight_kg",
            "cargo_volume_m3",
            "reference_number",
        }.issubset(shipment_columns)

        dvr_columns = {column["name"] for column in inspector.get_columns("delivery_variance_reports")}
        assert {"fault_assignment", "severity", "resolution_notes", "updated_at"}.issubset(dvr_columns)
    finally:
        engine.dispose()
        get_settings.cache_clear()
