from fastapi import APIRouter, Depends

from app.core.dependencies import AuthContext, require_permissions

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("")
def list_notifications(auth: AuthContext = Depends(require_permissions("read"))) -> dict[str, list[dict[str, str]]]:
    return {
        "items": [
            {
                "type": "system",
                "message": f"Notification center scaffold active for company {auth.company_id}",
            }
        ]
    }
