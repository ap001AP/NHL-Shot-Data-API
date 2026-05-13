from fastapi import FastAPI
from app.schemas import ShotRequest, ShotResponse
from app.model import predict_xg

app = FastAPI(
    title="NHL Expected Goals (xG) API",
    description="Predict the probability a shot results in a goal using a trained XGBoost model.",
    version="1.0.0",
)

@app.get("/health")
def health():
    return {"status": "ok", "model": "xg_model v1.0.0"}

@app.post("/predict", response_model=ShotResponse)
def predict(shot: ShotRequest):
    prob, is_high_danger, distance, angle = predict_xg(
        shot.x_coord,
        shot.y_coord,
        shot.shot_type,
        shot.away_skaters,
        shot.home_skaters,
        shot.period,
    )
    return ShotResponse(
        goal_probability=prob,
        is_high_danger=is_high_danger,
        distance=distance,
        angle=angle,
    )