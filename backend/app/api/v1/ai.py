from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.ai.delay_prediction import DelayPredictionInput, heuristic_delay_prediction
from app.core.dependencies import AuthContext, require_permission

router = APIRouter(prefix="/ai", tags=["ai"])


class AIQuery(BaseModel):
    question: str


class DelayPredictionRequest(BaseModel):
    distance_km: float
    cargo_weight_kg: float
    driver_on_time_rate: float
    route_traffic_score: float
    is_raining: bool = False


@router.post("/chat")
def chat(
    payload: AIQuery,
    auth: AuthContext = Depends(require_permission("analytics", "read")),
) -> dict[str, str]:
    return {
        "answer": (
            f"Copilot scaffold response for {auth.company_id}. "
            "Integrate SQL tool execution and retrieval-augmented context before production rollout."
        ),
        "question": payload.question,
    }


@router.post("/predict-delay")
def predict_delay(
    payload: DelayPredictionRequest,
    auth: AuthContext = Depends(require_permission("analytics", "read")),
) -> dict[str, float | int | bool]:
    result = heuristic_delay_prediction(DelayPredictionInput(**payload.model_dump()))
    return {
        "company_id": auth.company_id,
        "will_delay": result.will_delay,
        "confidence": result.confidence,
        "predicted_delay_minutes": result.predicted_delay_minutes,
    }
