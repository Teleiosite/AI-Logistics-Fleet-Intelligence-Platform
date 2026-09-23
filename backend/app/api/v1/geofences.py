from math import asin, cos, radians, sin, sqrt

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import AuthContext, require_permission
from app.db.session import get_db
from app.models.entities import Geofence
from app.schemas.geofence import GeofenceCreate, GeofenceRead
from app.schemas.location import LocationPingCreate

router = APIRouter(prefix="/geofences", tags=["geofences"])


def _distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    earth_radius = 6_371_000
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    return earth_radius * 2 * asin(sqrt(a))


@router.post("", response_model=GeofenceRead, status_code=201)
def create_geofence(
    payload: GeofenceCreate,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("fleet", "write")),
) -> GeofenceRead:
    geofence = Geofence(company_id=auth.company_id, **payload.model_dump())
    db.add(geofence)
    db.commit()
    db.refresh(geofence)
    return GeofenceRead.model_validate(geofence)


@router.get("", response_model=list[GeofenceRead])
def list_geofences(
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("fleet", "read")),
) -> list[GeofenceRead]:
    rows = db.scalars(select(Geofence).where(Geofence.company_id == auth.company_id, Geofence.is_active.is_(True)))
    return [GeofenceRead.model_validate(row) for row in rows]


@router.post("/check")
def check_geofences(
    payload: LocationPingCreate,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("fleet", "read")),
) -> dict[str, list[dict[str, float | str]]]:
    fences = db.scalars(select(Geofence).where(Geofence.company_id == auth.company_id, Geofence.is_active.is_(True)))
    matches = []
    for fence in fences:
        distance = _distance_meters(float(payload.latitude), float(payload.longitude), float(fence.latitude), float(fence.longitude))
        if distance <= float(fence.radius_meters):
            matches.append({"id": fence.id, "name": fence.name, "distance_meters": round(distance, 2)})
    return {"matches": matches}
