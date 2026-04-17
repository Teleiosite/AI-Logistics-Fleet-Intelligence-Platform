from dataclasses import dataclass


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
