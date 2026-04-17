from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.dependencies import AuthContext, require_permissions
from app.db.session import get_db
from app.models.entities import Shipment, ShipmentStatus, ShipmentStatusLog
from app.schemas.shipment import ShipmentCreate, ShipmentPODUpdate, ShipmentRead, ShipmentStatusUpdate
from app.services.crud import create_shipment, list_shipments

router = APIRouter(prefix="/shipments", tags=["shipments"])

VALID_TRANSITIONS: dict[ShipmentStatus, set[ShipmentStatus]] = {
    ShipmentStatus.DRAFT: {ShipmentStatus.SCHEDULED, ShipmentStatus.ASSIGNED},
    ShipmentStatus.SCHEDULED: {ShipmentStatus.ASSIGNED},
    ShipmentStatus.ASSIGNED: {ShipmentStatus.DISPATCHED},
    ShipmentStatus.DISPATCHED: {ShipmentStatus.EN_ROUTE_TO_PICKUP},
    ShipmentStatus.EN_ROUTE_TO_PICKUP: {ShipmentStatus.AT_PICKUP, ShipmentStatus.DELAYED},
    ShipmentStatus.AT_PICKUP: {ShipmentStatus.LOADED},
    ShipmentStatus.LOADED: {ShipmentStatus.IN_TRANSIT},
    ShipmentStatus.IN_TRANSIT: {ShipmentStatus.AT_DELIVERY, ShipmentStatus.DELAYED, ShipmentStatus.EXCEPTION},
    ShipmentStatus.AT_DELIVERY: {ShipmentStatus.UNLOADING},
    ShipmentStatus.UNLOADING: {ShipmentStatus.DELIVERED},
    ShipmentStatus.DELAYED: {ShipmentStatus.IN_TRANSIT, ShipmentStatus.EXCEPTION},
    ShipmentStatus.EXCEPTION: {ShipmentStatus.IN_TRANSIT, ShipmentStatus.DELAYED},
    ShipmentStatus.DELIVERED: set(),
}


@router.post("", response_model=ShipmentRead, status_code=status.HTTP_201_CREATED)
def create_shipment_endpoint(
    payload: ShipmentCreate,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permissions("write")),
) -> ShipmentRead:
    try:
        entity = create_shipment(db, auth.company_id, payload)
    except IntegrityError as exc:
        raise HTTPException(status_code=400, detail="Shipment number must be unique") from exc
    return ShipmentRead.model_validate(entity)


@router.get("", response_model=list[ShipmentRead])
def list_shipments_endpoint(
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permissions("read")),
) -> list[ShipmentRead]:
    return [ShipmentRead.model_validate(shipment) for shipment in list_shipments(db, auth.company_id)]


@router.post("/{shipment_id}/status", response_model=ShipmentRead)
def update_status(
    shipment_id: str,
    payload: ShipmentStatusUpdate,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permissions("write")),
) -> ShipmentRead:
    shipment = db.scalar(select(Shipment).where(Shipment.id == shipment_id, Shipment.company_id == auth.company_id))
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    try:
        requested_status = ShipmentStatus(payload.status)
    except ValueError as exc:
        valid_states = [state.value for state in ShipmentStatus]
        raise HTTPException(status_code=400, detail=f"Invalid status. Valid statuses: {valid_states}") from exc

    if requested_status == ShipmentStatus.DISPATCHED and (not shipment.vehicle_id or not shipment.driver_id):
        raise HTTPException(status_code=400, detail="Vehicle and driver must be assigned before dispatch")

    if requested_status == ShipmentStatus.DELIVERED and not (
        shipment.proof_of_delivery_url or shipment.delivery_signature_url
    ):
        raise HTTPException(status_code=400, detail="Proof of delivery photo or signature is required")

    if requested_status not in VALID_TRANSITIONS[shipment.status]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid transition from {shipment.status.value} to {requested_status.value}",
        )

    log = ShipmentStatusLog(
        shipment_id=shipment.id,
        from_status=shipment.status.value,
        to_status=requested_status.value,
        notes=payload.notes,
    )
    shipment.status = requested_status
    db.add(log)
    db.add(shipment)
    db.commit()
    db.refresh(shipment)
    return ShipmentRead.model_validate(shipment)


@router.post("/{shipment_id}/proof-of-delivery", response_model=ShipmentRead)
def upload_pod(
    shipment_id: str,
    payload: ShipmentPODUpdate,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permissions("write")),
) -> ShipmentRead:
    shipment = db.scalar(select(Shipment).where(Shipment.id == shipment_id, Shipment.company_id == auth.company_id))
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    shipment.proof_of_delivery_url = payload.proof_of_delivery_url
    shipment.delivery_signature_url = payload.delivery_signature_url
    db.add(shipment)
    db.commit()
    db.refresh(shipment)
    return ShipmentRead.model_validate(shipment)


@router.get("/{shipment_id}/timeline")
def shipment_timeline(
    shipment_id: str,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permissions("read")),
) -> list[dict[str, str | None]]:
    shipment = db.scalar(select(Shipment).where(Shipment.id == shipment_id, Shipment.company_id == auth.company_id))
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    logs = list(
        db.scalars(select(ShipmentStatusLog).where(ShipmentStatusLog.shipment_id == shipment_id).order_by(ShipmentStatusLog.created_at))
    )
    return [
        {
            "from_status": log.from_status,
            "to_status": log.to_status,
            "notes": log.notes,
            "created_at": log.created_at.isoformat(),
        }
        for log in logs
    ]
