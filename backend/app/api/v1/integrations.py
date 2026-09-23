import hashlib
import hmac

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.dependencies import AuthContext, require_permission
from app.integrations import configured_integrations

router = APIRouter(prefix="/integrations", tags=["integrations"])


@router.get("/status")
def integration_status(
    _auth: AuthContext = Depends(require_permission("system", "read")),
) -> dict[str, list[dict[str, str | bool]]]:
    return {"items": [status.__dict__ for status in configured_integrations(get_settings())]}


class TelematicsLocationEvent(BaseModel):
    company_id: str
    vehicle_id: str
    latitude: float
    longitude: float
    recorded_at: str | None = None


@router.post("/telematics/location")
def receive_telematics_location(
    event: TelematicsLocationEvent,
    x_signature: str | None = Header(default=None),
) -> dict[str, str]:
    """Validate an HMAC-signed telematics event before queueing it downstream."""
    secret = get_settings().telematics_webhook_secret
    if not secret or not x_signature:
        raise HTTPException(status_code=503, detail="Telematics webhook is not configured")
    digest = hmac.new(secret.encode(), event.model_dump_json().encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(digest, x_signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
    return {"status": "accepted", "vehicle_id": event.vehicle_id}
