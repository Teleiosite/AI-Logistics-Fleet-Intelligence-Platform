from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel as _BaseModel
from sqlalchemy.orm import Session

from app.core.dependencies import AuthContext, require_permission
from app.db.session import get_db
from app.schemas.dvr import DVRCreate, DVRRead
from app.services.crud import create_dvr, list_dvrs, update_dvr_status

router = APIRouter(prefix="/dvr", tags=["dvr"])


class DVRStatusUpdate(_BaseModel):
    status: str
    resolution_notes: str | None = None
    fault_assignment: str | None = None


@router.post("", response_model=DVRRead, status_code=status.HTTP_201_CREATED)
def create_dvr_endpoint(
    payload: DVRCreate,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("dvr", "write")),
) -> DVRRead:
    dvr = create_dvr(db, auth.company_id, payload)
    return DVRRead.model_validate(dvr)


@router.get("", response_model=list[DVRRead])
def list_dvr_endpoint(
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("dvr", "read")),
) -> list[DVRRead]:
    return [DVRRead.model_validate(item) for item in list_dvrs(db, auth.company_id)]


@router.patch("/{dvr_id}/status", response_model=DVRRead)
def update_dvr_status_endpoint(
    dvr_id: str,
    payload: DVRStatusUpdate,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("dvr", "write")),
) -> DVRRead:
    dvr = update_dvr_status(db, auth.company_id, dvr_id, payload.status, payload.resolution_notes, payload.fault_assignment)
    if not dvr:
        raise HTTPException(status_code=404, detail="DVR not found")
    return DVRRead.model_validate(dvr)
