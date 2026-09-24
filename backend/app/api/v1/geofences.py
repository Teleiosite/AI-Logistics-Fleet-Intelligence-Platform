from math import asin, cos, radians, sin, sqrt

import asyncio
import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import AuthContext, require_permission
from app.db.session import get_db
from app.models.entities import Geofence, GeofenceEvent
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
            db.add(GeofenceEvent(
                company_id=auth.company_id,
                geofence_id=fence.id,
                vehicle_id=payload.vehicle_id,
                event_type="inside",
                distance_meters=round(distance, 2),
            ))
    db.commit()
    return {"matches": matches}


@router.get("/events/stream")
async def stream_geofence_events(
    auth: AuthContext = Depends(require_permission("fleet", "read")),
    db: Session = Depends(get_db),
) -> StreamingResponse:
    async def events():
        rows = db.scalars(
            select(GeofenceEvent)
            .where(GeofenceEvent.company_id == auth.company_id)
            .order_by(GeofenceEvent.created_at.desc())
            .limit(20)
        )
        for row in reversed(list(rows)):
            yield f"data: {json.dumps({'id': row.id, 'vehicle_id': row.vehicle_id, 'geofence_id': row.geofence_id, 'event_type': row.event_type, 'created_at': row.created_at.isoformat()})}\n\n"
        await asyncio.sleep(0)

    return StreamingResponse(events(), media_type="text/event-stream")
