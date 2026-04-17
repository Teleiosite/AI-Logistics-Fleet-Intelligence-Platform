from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.dependencies import AuthContext, require_permissions

router = APIRouter(prefix="/ai", tags=["ai"])


class AIQuery(BaseModel):
    question: str


@router.post("/chat")
def chat(
    payload: AIQuery,
    auth: AuthContext = Depends(require_permissions("read")),
) -> dict[str, str]:
    return {
        "answer": (
            f"Copilot scaffold response for {auth.company_id}. "
            "Integrate model inference and SQL guardrails before production rollout."
        ),
        "question": payload.question,
    }
