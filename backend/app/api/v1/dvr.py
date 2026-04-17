from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import AuthContext, require_permission
from app.db.session import get_db
from app.schemas.dvr import DVRCreate, DVRRead
from app.services.crud import create_dvr, list_dvrs

router = APIRouter(prefix="/dvr", tags=["dvr"])


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
