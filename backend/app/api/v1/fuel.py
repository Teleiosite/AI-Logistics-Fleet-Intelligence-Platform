from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import AuthContext, require_permission
from app.db.session import get_db
from app.schemas.fuel import FuelLogCreate, FuelLogRead
from app.schemas.fuel_price import FuelPriceCreate, FuelPriceRead
from app.services.crud import create_fuel_log, create_fuel_price, list_fuel_logs, list_fuel_prices

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


@router.post("/prices", response_model=FuelPriceRead, status_code=status.HTTP_201_CREATED)
def create_fuel_price_endpoint(
    payload: FuelPriceCreate,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("fuel", "write")),
) -> FuelPriceRead:
    price = create_fuel_price(db, auth.company_id, payload)
    return FuelPriceRead.model_validate(price)


@router.get("/prices", response_model=list[FuelPriceRead])
def list_fuel_prices_endpoint(
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("fuel", "read")),
) -> list[FuelPriceRead]:
    return [FuelPriceRead.model_validate(item) for item in list_fuel_prices(db, auth.company_id)]
