from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
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


@router.get("/metrics/prometheus", response_class=PlainTextResponse)
def prometheus_metrics() -> str:
    lines = []
    for key, count in metrics_snapshot().items():
        method, path, status = key.split(" ", 2)
        safe_path = path.replace("/", "_").replace("-", "_") or "root"
        lines.append(
            f'fleetiq_http_requests_total{{method="{method}",path="{safe_path}",status="{status}"}} {count}'
        )
    return "\n".join(lines) + ("\n" if lines else "")
