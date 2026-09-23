from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.common import HealthResponse
from app.db.session import get_db
from app.core.logging import metrics_snapshot

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="fleetiq-api")


@router.get("/ready")
def readiness(db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        return {"status": "not_ready", "database": "unavailable"}
    return {"status": "ready", "database": "ok"}


@router.get("/metrics")
def metrics() -> dict[str, dict[str, int]]:
    return {"requests": metrics_snapshot()}
