from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core.dependencies import AuthContext, require_permission
from app.db.session import get_db
from app.models.entities import DeviceToken, User
from app.schemas.device import DeviceTokenCreate

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
def register_device(
    payload: DeviceTokenCreate,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("system", "read")),
) -> None:
    user = db.scalar(select(User).where(User.email == auth.email, User.company_id == auth.company_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    existing = db.scalar(select(DeviceToken).where(DeviceToken.token == payload.token))
    if existing:
        if existing.user_id != user.id or existing.company_id != auth.company_id:
            raise HTTPException(status_code=409, detail="Device token belongs to another tenant")
        existing.platform = payload.platform
    else:
        db.add(DeviceToken(user_id=user.id, company_id=auth.company_id, **payload.model_dump()))
    db.commit()


@router.delete("/{token}", status_code=status.HTTP_204_NO_CONTENT)
def unregister_device(
    token: str,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("system", "read")),
) -> None:
    db.execute(delete(DeviceToken).where(DeviceToken.token == token, DeviceToken.company_id == auth.company_id))
    db.commit()
