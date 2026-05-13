import joblib
import math
import numpy as np
from pathlib import Path

MODEL_DIR = Path(__file__).parent.parent / "model"

model = joblib.load(MODEL_DIR / "xg_model.joblib")
encoder = joblib.load(MODEL_DIR / "shot_type_encoder.joblib")
feature_names = joblib.load(MODEL_DIR / "feature_names.joblib")

def compute_features(x: float, y: float, shot_type: str,
                     away_skaters: int, home_skaters: int, period: int) -> np.ndarray:
    distance = ((abs(x) - 89) ** 2 + y ** 2) ** 0.5
    angle = abs(math.degrees(math.atan2(abs(y), abs(abs(x) - 89))))
    is_power_play = int(away_skaters != home_skaters)
    is_shorthanded = int(away_skaters < home_skaters)
    is_slot = int(distance < 20 and angle < 45)
    is_overtime = int(period > 3)

    try:
        shot_type_enc = encoder.transform([shot_type])[0]
    except ValueError:
        shot_type_enc = encoder.transform(["unknown"])[0]

    features = {
        "distance": distance,
        "angle": angle,
        "shot_type_enc": shot_type_enc,
        "is_power_play": is_power_play,
        "is_shorthanded": is_shorthanded,
        "away_skaters": away_skaters,
        "home_skaters": home_skaters,
        "is_slot": is_slot,
        "is_overtime": is_overtime,
        "period": period,
    }

    return np.array([[features[f] for f in feature_names]]), distance, angle, bool(is_slot)

def predict_xg(x, y, shot_type, away_skaters, home_skaters, period):
    feature_array, distance, angle, is_slot = compute_features(
        x, y, shot_type, away_skaters, home_skaters, period
    )
    prob = float(model.predict_proba(feature_array)[0][1])
    return round(prob, 4), is_slot, round(distance, 2), round(angle, 2)