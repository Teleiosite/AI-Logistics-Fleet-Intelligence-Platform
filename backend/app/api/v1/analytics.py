from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import AuthContext, require_permissions
from app.db.session import get_db
from app.services.crud import get_shipment_metrics

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/shipments")
def shipment_metrics(
    db: Session = Depends(get_db), auth: AuthContext = Depends(require_permissions("read"))
) -> dict[str, int]:
    return get_shipment_metrics(db, auth.company_id)
