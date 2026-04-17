from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import AuthContext, require_permission
from app.db.session import get_db
from app.schemas.fuel import FuelLogCreate, FuelLogRead
from app.services.crud import create_fuel_log, list_fuel_logs

router = APIRouter(prefix="/fuel", tags=["fuel"])


@router.post("", response_model=FuelLogRead, status_code=status.HTTP_201_CREATED)
def create_fuel_log_endpoint(
    payload: FuelLogCreate,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("fuel", "write")),
) -> FuelLogRead:
    log = create_fuel_log(db, auth.company_id, payload)
    return FuelLogRead.model_validate(log)


@router.get("", response_model=list[FuelLogRead])
def list_fuel_logs_endpoint(
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("fuel", "read")),
) -> list[FuelLogRead]:
    return [FuelLogRead.model_validate(item) for item in list_fuel_logs(db, auth.company_id)]


@router.get("/anomalies", response_model=list[FuelLogRead])
def list_anomalies_endpoint(
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("fuel", "read")),
) -> list[FuelLogRead]:
    return [FuelLogRead.model_validate(item) for item in list_fuel_logs(db, auth.company_id) if item.is_anomaly]
