"""Train the delay model from a CSV dataset exported from shipment history."""

from pathlib import Path

import joblib
import numpy as np
import csv
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = Path(__file__).resolve().parent / "delay_model.joblib"


def train(dataset_path: Path | None = None) -> None:
    if dataset_path is None:
        raise ValueError("A historical shipment CSV path is required")
    rows = list(csv.DictReader(dataset_path.open(newline="", encoding="utf-8")))
    required = {"distance_km", "cargo_weight_kg", "driver_on_time_rate", "route_traffic_score", "is_raining", "was_delayed"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError(f"Dataset must contain: {', '.join(sorted(required))}")
    X = np.array([[float(row[key]) for key in (
        "distance_km", "cargo_weight_kg", "driver_on_time_rate", "route_traffic_score", "is_raining"
    )] for row in rows])
    y = np.array([int(row["was_delayed"]) for row in rows])
    if len(set(y.tolist())) < 2:
        raise ValueError("Dataset must contain both delayed and on-time examples")

    model = RandomForestClassifier(n_estimators=120, random_state=42)
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", type=Path)
    train(parser.parse_args().dataset)
