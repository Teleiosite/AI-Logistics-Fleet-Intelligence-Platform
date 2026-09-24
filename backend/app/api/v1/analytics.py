from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import AuthContext, require_permission
from app.db.session import get_db
from app.services.crud import (
    get_dvr_metrics,
    get_fleet_metrics,
    get_fuel_metrics,
    get_shipment_metrics,
    get_shipment_trend,
)

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/shipments")
def shipment_metrics(
    db: Session = Depends(get_db), auth: AuthContext = Depends(require_permission("analytics", "read"))
) -> dict[str, int]:
    return get_shipment_metrics(db, auth.company_id)


@router.get("/fuel")
def fuel_metrics(
    db: Session = Depends(get_db), auth: AuthContext = Depends(require_permission("analytics", "read"))
) -> dict:
    return get_fuel_metrics(db, auth.company_id)


@router.get("/fleet")
def fleet_metrics(
    db: Session = Depends(get_db), auth: AuthContext = Depends(require_permission("analytics", "read"))
) -> dict:
    return get_fleet_metrics(db, auth.company_id)


@router.get("/dvr")
def dvr_metrics(
    db: Session = Depends(get_db), auth: AuthContext = Depends(require_permission("analytics", "read"))
) -> dict:
    return get_dvr_metrics(db, auth.company_id)


@router.get("/shipments/trend")
def shipment_trend(
    db: Session = Depends(get_db), auth: AuthContext = Depends(require_permission("analytics", "read"))
) -> list[dict]:
    return get_shipment_trend(db, auth.company_id)
