from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.dependencies import AuthContext, require_permission
from app.tasks.notifications import send_email_notification

router = APIRouter(prefix="/notifications", tags=["notifications"])


class NotificationRequest(BaseModel):
    recipient: str
    subject: str
    message: str


@router.get("")
def list_notifications(auth: AuthContext = Depends(require_permission("notifications", "read"))) -> dict[str, list[dict[str, str]]]:
    return {
        "items": [
            {
                "type": "system",
                "message": f"Notification center scaffold active for company {auth.company_id}",
            }
        ]
    }


@router.post("/test")
def send_test_notification(
    payload: NotificationRequest,
    auth: AuthContext = Depends(require_permission("notifications", "write")),
) -> dict[str, str]:
    async_result = send_email_notification.delay(payload.recipient, payload.subject, payload.message)
    return {"task_id": async_result.id, "status": "queued", "company_id": auth.company_id}
