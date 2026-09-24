from pathlib import Path
from dataclasses import dataclass

import joblib


@dataclass
class DelayPredictionInput:
    distance_km: float
    cargo_weight_kg: float
    driver_on_time_rate: float
    route_traffic_score: float
    is_raining: bool


@dataclass
class DelayPredictionOutput:
    will_delay: bool
    confidence: float
    predicted_delay_minutes: int


def heuristic_delay_prediction(data: DelayPredictionInput) -> DelayPredictionOutput:
    risk = 0.0
    risk += min(data.distance_km / 500, 1.0) * 0.25
    risk += min(data.cargo_weight_kg / 30000, 1.0) * 0.2
    risk += (1 - max(0.0, min(data.driver_on_time_rate, 1.0))) * 0.25
    risk += max(0.0, min(data.route_traffic_score, 1.0)) * 0.2
    risk += 0.1 if data.is_raining else 0.0

    confidence = max(0.5, min(0.98, 0.5 + risk / 2))
    predicted_delay = int(risk * 120)
    return DelayPredictionOutput(will_delay=risk >= 0.55, confidence=round(confidence, 2), predicted_delay_minutes=predicted_delay)


def predict_delay(data: DelayPredictionInput) -> DelayPredictionOutput:
    """Use the trained model when present and retain a deterministic safe fallback."""
    model_path = Path(__file__).with_name("delay_model.joblib")
    if model_path.exists():
        try:
            model = joblib.load(model_path)
            features = [[
                data.distance_km,
                data.cargo_weight_kg,
                data.driver_on_time_rate,
                data.route_traffic_score,
                float(data.is_raining),
            ]]
            probabilities = model.predict_proba(features)[0]
            delayed_probability = float(probabilities[1])
            return DelayPredictionOutput(
                will_delay=delayed_probability >= 0.5,
                confidence=round(max(probabilities), 2),
                predicted_delay_minutes=round(delayed_probability * 120),
            )
        except (OSError, ValueError, IndexError, AttributeError):
            pass
    return heuristic_delay_prediction(data)
