"""End-to-end integration tests covering all major API workflows.

These tests use an in-memory SQLite database and the FastAPI TestClient so they
run without any external services (Postgres, Redis, Celery).
"""

from datetime import datetime
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models import entities  # noqa: F401 – ensure all SQLAlchemy models are registered
from app.core.rate_limit import rate_limiter


# ---------------------------------------------------------------------------
# Test database / client fixtures
# ---------------------------------------------------------------------------

TEST_DB_URL = "sqlite+pysqlite:///file:testdb?mode=memory&cache=shared&uri=true"


@pytest.fixture(scope="module", autouse=True)
def clear_rate_limiter():
    """Reset the in-memory rate limiter before the test module runs."""
    rate_limiter._events.clear()
    yield
    rate_limiter._events.clear()


@pytest.fixture(scope="module")
def db_engine():
    eng = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=eng)
    yield eng
    Base.metadata.drop_all(bind=eng)
    eng.dispose()


@pytest.fixture(scope="module")
def client(db_engine):
    TestingSession = sessionmaker(bind=db_engine, autoflush=False, autocommit=False)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Helper: register a company + user, return token
# ---------------------------------------------------------------------------

_company_counter = 0


def _create_company_and_user(client: TestClient, role: str = "company_admin") -> tuple[str, str, str]:
    """Returns (company_id, user_email, bearer_token)."""
    global _company_counter
    _company_counter += 1
    idx = _company_counter

    slug = f"test-co-{idx}"
    email = f"user-{idx}@test.example"

    # Reset rate limiter for this test to avoid hitting auth limits during testing
    rate_limiter._events.clear()

    # Create company
    resp = client.post("/api/v1/companies", json={"name": f"Test Company {idx}", "slug": slug})
    assert resp.status_code == 201, resp.text
    company_id = resp.json()["id"]

    # Register user
    resp = client.post(
        "/api/v1/auth/register",
        json={
            "company_id": company_id,
            "email": email,
            "password": "TestPass123!",
            "first_name": "Test",
            "last_name": "User",
            "role": role,
        },
    )
    assert resp.status_code == 201, resp.text
    token = resp.json()["access_token"]
    return company_id, email, token


# ===========================================================================
# 1. Health
# ===========================================================================


def test_health(client: TestClient) -> None:
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "fleetiq" in data["service"].lower()


# ===========================================================================
# 2. Auth workflow: register → login → /me
# ===========================================================================


def test_auth_workflow(client: TestClient) -> None:
    company_id, email, token = _create_company_and_user(client)

    # Login
    resp = client.post("/api/v1/auth/login", json={"email": email, "password": "TestPass123!"})
    assert resp.status_code == 200
    login_token = resp.json()["access_token"]
    assert login_token

    # /me
    resp = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer " + token})
    assert resp.status_code == 200
    me = resp.json()
    assert me["email"] == email
    assert me["company_id"] == company_id
    assert me["role"] == "company_admin"


def test_login_invalid_credentials(client: TestClient) -> None:
    resp = client.post("/api/v1/auth/login", json={"email": "no-such@user.com", "password": "wrong"})
    assert resp.status_code == 401


def test_protected_endpoint_without_token(client: TestClient) -> None:
    resp = client.get("/api/v1/analytics/shipments")
    # HTTPBearer with auto_error=True returns 403 when no Authorization header present
    assert resp.status_code in (401, 403)


# ===========================================================================
# 3. Companies
# ===========================================================================


def test_create_company_duplicate_slug(client: TestClient) -> None:
    client.post("/api/v1/companies", json={"name": "DupCo", "slug": "dup-slug"})
    resp = client.post("/api/v1/companies", json={"name": "DupCo2", "slug": "dup-slug"})
    assert resp.status_code == 400


# ===========================================================================
# 4. Fleet: vehicles + drivers + transporters
# ===========================================================================


def test_fleet_workflow(client: TestClient) -> None:
    company_id, _, token = _create_company_and_user(client)
    auth = {"Authorization": "Bearer " + token}

    # Create vehicle
    resp = client.post(
        "/api/v1/vehicles",
        json={"vehicle_number": "VH-T01", "license_plate": f"TST-001-{company_id[:4]}", "vehicle_type": "truck", "tank_capacity_liters": "500"},
        headers=auth,
    )
    assert resp.status_code == 201
    vehicle = resp.json()
    assert vehicle["license_plate"].startswith("TST")

    # List vehicles
    resp = client.get("/api/v1/vehicles", headers=auth)
    assert resp.status_code == 200
    assert any(v["id"] == vehicle["id"] for v in resp.json())

    # Create driver
    resp = client.post(
        "/api/v1/drivers",
        json={"first_name": "Test", "last_name": "Driver", "phone": "+2348000000001", "license_number": f"DRV-TST-{company_id[:6]}"},
        headers=auth,
    )
    assert resp.status_code == 201
    driver = resp.json()

    # List drivers
    resp = client.get("/api/v1/drivers", headers=auth)
    assert resp.status_code == 200
    assert any(d["id"] == driver["id"] for d in resp.json())

    # Create transporter
    resp = client.post(
        "/api/v1/transporters",
        json={"name": "Test Haulage", "contact_person": "Mr Test"},
        headers=auth,
    )
    assert resp.status_code == 201


# ===========================================================================
# 5. Shipment lifecycle
# ===========================================================================


def test_shipment_lifecycle(client: TestClient) -> None:
    company_id, _, token = _create_company_and_user(client)
    auth = {"Authorization": "Bearer " + token}

    # Setup vehicle + driver first
    v_resp = client.post(
        "/api/v1/vehicles",
        json={"vehicle_number": "VH-SHP", "license_plate": f"SHP-{company_id[:4]}", "vehicle_type": "truck"},
        headers=auth,
    )
    vehicle_id = v_resp.json()["id"]

    d_resp = client.post(
        "/api/v1/drivers",
        json={"first_name": "Ship", "last_name": "Driver", "phone": "+2348000000002", "license_number": f"DRV-SHP-{company_id[:6]}"},
        headers=auth,
    )
    driver_id = d_resp.json()["id"]

    # Create shipment
    resp = client.post(
        "/api/v1/shipments",
        json={
            "shipment_number": f"SHP-{company_id[:8]}",
            "customer_name": "Test Customer",
            "pickup_address": "Lagos",
            "delivery_address": "Abuja",
            "vehicle_id": vehicle_id,
            "driver_id": driver_id,
        },
        headers=auth,
    )
    assert resp.status_code == 201
    shipment = resp.json()
    assert shipment["status"] == "draft"
    assert "created_at" in shipment
    shipment_id = shipment["id"]

    # List shipments
    resp = client.get("/api/v1/shipments", headers=auth)
    assert resp.status_code == 200
    assert any(s["id"] == shipment_id for s in resp.json())

    # Progress status: draft → scheduled → assigned → dispatched
    for new_status in ("scheduled", "assigned", "dispatched"):
        resp = client.post(
            f"/api/v1/shipments/{shipment_id}/status",
            json={"status": new_status, "notes": f"Moving to {new_status}"},
            headers=auth,
        )
        assert resp.status_code == 200, f"Failed transition to {new_status}: {resp.text}"
        assert resp.json()["status"] == new_status

    # Timeline
    resp = client.get(f"/api/v1/shipments/{shipment_id}/timeline", headers=auth)
    assert resp.status_code == 200
    timeline = resp.json()
    assert len(timeline) >= 2

    # Upload proof-of-delivery URL
    resp = client.post(
        f"/api/v1/shipments/{shipment_id}/proof-of-delivery",
        json={"proof_of_delivery_url": "https://example.com/pod/sample.jpg"},
        headers=auth,
    )
    assert resp.status_code == 200


# ===========================================================================
# 6. Fuel logs + anomaly detection
# ===========================================================================


def test_fuel_workflow(client: TestClient) -> None:
    company_id, _, token = _create_company_and_user(client)
    auth = {"Authorization": "Bearer " + token}

    # Create vehicle with known tank capacity
    v_resp = client.post(
        "/api/v1/vehicles",
        json={"vehicle_number": "VH-FUEL", "license_plate": f"FUEL-{company_id[:4]}", "vehicle_type": "truck", "tank_capacity_liters": "400"},
        headers=auth,
    )
    vehicle_id = v_resp.json()["id"]

    # Normal fill
    resp = client.post(
        "/api/v1/fuel",
        json={"vehicle_id": vehicle_id, "quantity_liters": "300", "price_per_liter": "700"},
        headers=auth,
    )
    assert resp.status_code == 201
    log = resp.json()
    assert not log["is_anomaly"]
    assert "created_at" in log
    assert Decimal(str(log["total_cost"])) == Decimal("210000")

    # Anomaly fill: > 110% of 400L tank
    resp = client.post(
        "/api/v1/fuel",
        json={"vehicle_id": vehicle_id, "quantity_liters": "500", "price_per_liter": "700"},
        headers=auth,
    )
    assert resp.status_code == 201
    anomaly_log = resp.json()
    assert anomaly_log["is_anomaly"]
    assert anomaly_log["anomaly_reason"] is not None

    # List all + anomaly filter
    resp = client.get("/api/v1/fuel", headers=auth)
    assert len(resp.json()) >= 2

    resp = client.get("/api/v1/fuel/anomalies", headers=auth)
    assert all(item["is_anomaly"] for item in resp.json())


# ===========================================================================
# 7. Invoice: create, upload-text OCR, auto-match, dispute-memo
# ===========================================================================


def test_invoice_workflow(client: TestClient) -> None:
    company_id, _, token = _create_company_and_user(client)
    auth = {"Authorization": "Bearer " + token}

    # Create invoice manually
    resp = client.post(
        "/api/v1/invoices",
        json={"invoice_number": "INV-TEST-001", "total_amount": "150000"},
        headers=auth,
    )
    assert resp.status_code == 200
    invoice = resp.json()
    assert invoice["status"] == "pending"

    # Upload invoice text (OCR path)
    raw_text = "Invoice Number: INV-OCR-001\nRoute Lagos-Abuja 120000.00\nHandling Fee 30000.00"
    resp = client.post(
        "/api/v1/invoices/upload-text",
        json={"raw_text": raw_text},
        headers=auth,
    )
    assert resp.status_code == 200
    ocr_invoice = resp.json()
    assert ocr_invoice["invoice_number"] == "INV-OCR-001"

    # List invoices
    resp = client.get("/api/v1/invoices", headers=auth)
    assert resp.status_code == 200
    assert len(resp.json()) >= 2

    # Auto-match
    resp = client.post(f"/api/v1/invoices/{ocr_invoice['id']}/auto-match", headers=auth)
    assert resp.status_code == 200
    match_result = resp.json()
    assert "matched" in match_result
    assert "discrepancies" in match_result

    # Dispute memo
    resp = client.get(f"/api/v1/invoices/{ocr_invoice['id']}/dispute-memo", headers=auth)
    assert resp.status_code == 200
    memo = resp.json()["memo"]
    assert "INV-OCR-001" in memo


# ===========================================================================
# 8. DVR
# ===========================================================================


def test_dvr_workflow(client: TestClient) -> None:
    company_id, _, token = _create_company_and_user(client)
    auth = {"Authorization": "Bearer " + token}

    # Need a shipment first
    v_resp = client.post(
        "/api/v1/vehicles",
        json={"vehicle_number": "VH-DVR", "license_plate": f"DVR-{company_id[:4]}", "vehicle_type": "truck"},
        headers=auth,
    )
    s_resp = client.post(
        "/api/v1/shipments",
        json={
            "shipment_number": f"SHP-DVR-{company_id[:8]}",
            "customer_name": "DVR Test",
            "pickup_address": "Lagos",
            "delivery_address": "Port Harcourt",
        },
        headers=auth,
    )
    shipment_id = s_resp.json()["id"]

    # Create DVR
    resp = client.post(
        "/api/v1/dvr",
        json={
            "shipment_id": shipment_id,
            "dvr_number": f"DVR-TST-{company_id[:8]}",
            "variance_type": "quantity_shortage",
            "description": "Shortage of 100kg detected at delivery.",
            "financial_impact": "5000.00",
        },
        headers=auth,
    )
    assert resp.status_code == 201
    dvr = resp.json()
    assert dvr["status"] == "open"

    # List DVRs
    resp = client.get("/api/v1/dvr", headers=auth)
    assert resp.status_code == 200
    assert any(d["id"] == dvr["id"] for d in resp.json())


# ===========================================================================
# 9. Analytics
# ===========================================================================


def test_analytics_shipment_metrics(client: TestClient) -> None:
    company_id, _, token = _create_company_and_user(client)
    auth = {"Authorization": "Bearer " + token}

    resp = client.get("/api/v1/analytics/shipments", headers=auth)
    assert resp.status_code == 200
    metrics = resp.json()
    assert "total_shipments" in metrics
    assert "active_shipments" in metrics
    assert "delayed_shipments" in metrics
    assert "delivered_shipments" in metrics
    assert metrics["total_shipments"] >= 0


# ===========================================================================
# 10. AI: delay prediction
# ===========================================================================


def test_ai_delay_prediction(client: TestClient) -> None:
    company_id, _, token = _create_company_and_user(client)
    auth = {"Authorization": "Bearer " + token}

    resp = client.post(
        "/api/v1/ai/predict-delay",
        json={
            "distance_km": 800,
            "cargo_weight_kg": 20000,
            "driver_on_time_rate": 0.6,
            "route_traffic_score": 0.7,
            "is_raining": True,
        },
        headers=auth,
    )
    assert resp.status_code == 200
    result = resp.json()
    assert "will_delay" in result
    assert "confidence" in result
    assert "predicted_delay_minutes" in result
    assert 0.0 <= result["confidence"] <= 1.0


# ===========================================================================
# 11. Notifications
# ===========================================================================


def test_notifications(client: TestClient) -> None:
    company_id, _, token = _create_company_and_user(client)
    auth = {"Authorization": "Bearer " + token}

    resp = client.get("/api/v1/notifications", headers=auth)
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data


# ===========================================================================
# 12. RBAC enforcement
# ===========================================================================


def test_driver_cannot_approve_invoices(client: TestClient) -> None:
    company_id, _, token = _create_company_and_user(client, role="driver")
    auth = {"Authorization": "Bearer " + token}

    # driver has no invoice:approve permission
    resp = client.post("/api/v1/invoices/some-id/auto-match", headers=auth)
    assert resp.status_code == 403


def test_auditor_cannot_write_shipments(client: TestClient) -> None:
    company_id, _, token = _create_company_and_user(client, role="auditor")
    auth = {"Authorization": "Bearer " + token}

    resp = client.post(
        "/api/v1/shipments",
        json={"shipment_number": "SHP-AUD-01", "customer_name": "Auditor", "pickup_address": "A", "delivery_address": "B"},
        headers=auth,
    )
    assert resp.status_code == 403


def test_shipment_with_cargo_details(client: TestClient) -> None:
    company_id, _, token = _create_company_and_user(client)
    auth = {"Authorization": "Bearer " + token}

    resp = client.post(
        "/api/v1/shipments",
        json={
            "shipment_number": f"SHP-CARGO-{company_id[:6]}",
            "customer_name": "Cargo Customer",
            "pickup_address": "Lagos",
            "delivery_address": "Kano",
            "priority": "express",
            "cargo_weight_kg": "2500.50",
            "reference_number": "REF-CARGO-001",
        },
        headers=auth,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["priority"] == "express"
    assert Decimal(str(data["cargo_weight_kg"])) == Decimal("2500.50")
    assert data["reference_number"] == "REF-CARGO-001"


def test_analytics_fuel(client: TestClient) -> None:
    company_id, _, token = _create_company_and_user(client)
    auth = {"Authorization": "Bearer " + token}

    vehicle_resp = client.post(
        "/api/v1/vehicles",
        json={"vehicle_number": "VH-AFUEL", "license_plate": f"AF-{company_id[:4]}", "vehicle_type": "truck", "tank_capacity_liters": "300"},
        headers=auth,
    )
    vehicle_id = vehicle_resp.json()["id"]

    fuel_resp = client.post(
        "/api/v1/fuel",
        json={"vehicle_id": vehicle_id, "quantity_liters": "120", "price_per_liter": "700", "odometer_reading_km": "1000"},
        headers=auth,
    )
    assert fuel_resp.status_code == 201

    resp = client.get("/api/v1/analytics/fuel", headers=auth)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_volume_liters"] > 0
    assert {"total_volume_liters", "total_cost", "anomaly_count", "avg_efficiency_lkm"}.issubset(data)


def test_analytics_fleet(client: TestClient) -> None:
    company_id, _, token = _create_company_and_user(client)
    auth = {"Authorization": "Bearer " + token}

    vehicle_resp = client.post(
        "/api/v1/vehicles",
        json={"vehicle_number": "VH-AFLT", "license_plate": f"FL-{company_id[:4]}", "vehicle_type": "truck"},
        headers=auth,
    )
    assert vehicle_resp.status_code == 201

    driver_resp = client.post(
        "/api/v1/drivers",
        json={"first_name": "Fleet", "last_name": "Driver", "phone": "+2348000000099", "license_number": f"DRV-FLT-{company_id[:6]}"},
        headers=auth,
    )
    assert driver_resp.status_code == 201

    resp = client.get("/api/v1/analytics/fleet", headers=auth)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_vehicles"] >= 1
    assert data["total_drivers"] >= 1
    assert data["active_vehicles"] >= 1
    assert data["active_drivers"] >= 1


def test_analytics_dvr(client: TestClient) -> None:
    company_id, _, token = _create_company_and_user(client)
    auth = {"Authorization": "Bearer " + token}

    shipment_resp = client.post(
        "/api/v1/shipments",
        json={
            "shipment_number": f"SHP-ADVR-{company_id[:6]}",
            "customer_name": "DVR Analytics",
            "pickup_address": "Ibadan",
            "delivery_address": "Jos",
        },
        headers=auth,
    )
    shipment_id = shipment_resp.json()["id"]

    dvr_resp = client.post(
        "/api/v1/dvr",
        json={
            "shipment_id": shipment_id,
            "dvr_number": f"DVR-AN-{company_id[:6]}",
            "variance_type": "delay",
            "description": "Unexpected delay",
        },
        headers=auth,
    )
    assert dvr_resp.status_code == 201

    resp = client.get("/api/v1/analytics/dvr", headers=auth)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1
    assert data["open"] >= 1
    assert isinstance(data["by_type"], list)


def test_shipment_trend(client: TestClient) -> None:
    company_id, _, token = _create_company_and_user(client)
    auth = {"Authorization": "Bearer " + token}

    resp = client.get("/api/v1/analytics/shipments/trend", headers=auth)
    assert resp.status_code == 200
    trend = resp.json()
    assert len(trend) == 7
    assert all({"date", "count"}.issubset(item) for item in trend)


def test_dvr_status_update(client: TestClient) -> None:
    company_id, _, token = _create_company_and_user(client)
    auth = {"Authorization": "Bearer " + token}

    shipment_resp = client.post(
        "/api/v1/shipments",
        json={
            "shipment_number": f"SHP-DVRS-{company_id[:6]}",
            "customer_name": "Status Customer",
            "pickup_address": "Aba",
            "delivery_address": "Enugu",
        },
        headers=auth,
    )
    shipment_id = shipment_resp.json()["id"]

    dvr_resp = client.post(
        "/api/v1/dvr",
        json={
            "shipment_id": shipment_id,
            "dvr_number": f"DVR-ST-{company_id[:6]}",
            "variance_type": "damage",
            "description": "Minor packaging damage",
        },
        headers=auth,
    )
    dvr_id = dvr_resp.json()["id"]

    resp = client.patch(
        f"/api/v1/dvr/{dvr_id}/status",
        json={"status": "resolved", "resolution_notes": "Handled", "fault_assignment": "driver"},
        headers=auth,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "resolved"
    assert data["resolution_notes"] == "Handled"
    assert data["fault_assignment"] == "driver"


def test_jwt_refresh(client: TestClient) -> None:
    company_id, email, token = _create_company_and_user(client)
    assert company_id
    assert token

    login_resp = client.post("/api/v1/auth/login", json={"email": email, "password": "TestPass123!"})
    assert login_resp.status_code == 200
    refresh_token = login_resp.json()["refresh_token"]

    resp = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200
    data = resp.json()
    assert data["access_token"]
    assert data["refresh_token"]


def test_fuel_price_history(client: TestClient) -> None:
    company_id, _, token = _create_company_and_user(client)
    auth = {"Authorization": "Bearer " + token}

    create_resp = client.post(
        "/api/v1/fuel/prices",
        json={"region": "North Central", "fuel_type": "diesel", "price_per_liter": "950.00"},
        headers=auth,
    )
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["region"] == "North Central"

    list_resp = client.get("/api/v1/fuel/prices", headers=auth)
    assert list_resp.status_code == 200
    prices = list_resp.json()
    assert any(item["id"] == created["id"] for item in prices)
