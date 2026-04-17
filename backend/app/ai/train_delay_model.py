"""Offline training stub for delay prediction model.

This script demonstrates the training pipeline structure requested in the FleetIQ roadmap.
It intentionally uses a synthetic dataset placeholder and can be replaced with production data.
"""

from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = Path(__file__).resolve().parent / "delay_model.joblib"


def train() -> None:
    rng = np.random.default_rng(42)
    X = rng.normal(size=(500, 5))
    y = (X[:, 0] + X[:, 1] * 0.5 + rng.normal(scale=0.4, size=500) > 0.2).astype(int)

    model = RandomForestClassifier(n_estimators=120, random_state=42)
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)


if __name__ == "__main__":
    train()
