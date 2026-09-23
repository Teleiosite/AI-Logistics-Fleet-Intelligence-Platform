from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.core.dependencies import AuthContext, require_permission
from app.db.session import get_db
from app.models.entities import Vehicle, VehicleLocationPing
from app.schemas.location import LocationPingCreate, LocationPingRead

router = APIRouter(prefix="/locations", tags=["locations"])


@router.post("", response_model=LocationPingRead, status_code=201)
def record_location(
    payload: LocationPingCreate,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("fleet", "write")),
) -> LocationPingRead:
    vehicle = db.scalar(select(Vehicle).where(Vehicle.id == payload.vehicle_id, Vehicle.company_id == auth.company_id))
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    ping = VehicleLocationPing(company_id=auth.company_id, **payload.model_dump(exclude_none=True))
    db.add(ping)
    db.commit()
    db.refresh(ping)
    return LocationPingRead.model_validate(ping)


@router.get("/{vehicle_id}", response_model=list[LocationPingRead])
def list_locations(
    vehicle_id: str,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("fleet", "read")),
) -> list[LocationPingRead]:
    rows = db.scalars(
        select(VehicleLocationPing)
        .where(VehicleLocationPing.vehicle_id == vehicle_id, VehicleLocationPing.company_id == auth.company_id)
        .order_by(desc(VehicleLocationPing.recorded_at))
        .limit(100)
    )
    return [LocationPingRead.model_validate(row) for row in rows]
