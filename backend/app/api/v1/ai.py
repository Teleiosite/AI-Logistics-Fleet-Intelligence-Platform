from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.ai.delay_prediction import DelayPredictionInput, predict_delay as predict_delay_model
from app.core.dependencies import AuthContext, require_permission
from app.db.session import get_db
from app.services.crud import get_dvr_metrics, get_fleet_metrics, get_fuel_metrics, get_shipment_metrics

router = APIRouter(prefix="/ai", tags=["ai"])


class AIQuery(BaseModel):
    question: str
    conversation_id: str | None = None


class DelayPredictionRequest(BaseModel):
    distance_km: float
    cargo_weight_kg: float
    driver_on_time_rate: float
    route_traffic_score: float
    is_raining: bool = False


@router.post("/chat")
def chat(
    payload: AIQuery,
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(require_permission("analytics", "read")),
) -> dict[str, object]:
    """Answer a constrained analytics question without exposing arbitrary SQL or tenant data."""
    question = payload.question.strip().lower()
    if not question or len(question) > 500:
        raise HTTPException(status_code=422, detail="Question must contain 1-500 characters")
    if any(token in question for token in ("select ", "insert ", "update ", "delete ", "drop ", "sql")):
        raise HTTPException(status_code=400, detail="Direct SQL queries are not supported")

    tools = {
        "shipment": get_shipment_metrics,
        "delivery": get_shipment_metrics,
        "fuel": get_fuel_metrics,
        "fleet": get_fleet_metrics,
        "vehicle": get_fleet_metrics,
        "dvr": get_dvr_metrics,
        "variance": get_dvr_metrics,
    }
    selected = next((tool for keyword, tool in tools.items() if keyword in question), None)
    if selected is None:
        raise HTTPException(
            status_code=400,
            detail="Ask about shipments, fuel, fleet, vehicles, DVRs, or delivery performance",
        )
    result = selected(db, auth.company_id)
    summary = ", ".join(f"{key.replace('_', ' ')}: {value}" for key, value in result.items())
    return {
        "answer": f"Here is the latest company-scoped {selected.__name__.removeprefix('get_').replace('_', ' ')} summary: {summary}.",
        "question": payload.question,
        "conversation_id": payload.conversation_id,
        "data": result,
    }


@router.post("/predict-delay")
def predict_delay(
    payload: DelayPredictionRequest,
    auth: AuthContext = Depends(require_permission("analytics", "read")),
) -> dict:
    result = predict_delay_model(DelayPredictionInput(**payload.model_dump()))
    return {
        "company_id": auth.company_id,
        "will_delay": result.will_delay,
        "confidence": result.confidence,
        "predicted_delay_minutes": result.predicted_delay_minutes,
    }
