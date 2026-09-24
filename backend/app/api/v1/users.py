from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import AuthContext, require_permission
from app.db.session import get_db
from app.schemas.user import UserRead
from app.services.crud import list_users

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserRead])
def get_users(
    auth: AuthContext = Depends(require_permission("system", "read")),
    db: Session = Depends(get_db),
) -> list[UserRead]:
    """Return active users belonging to the authenticated user's company."""
    return list_users(db, auth.company_id)
