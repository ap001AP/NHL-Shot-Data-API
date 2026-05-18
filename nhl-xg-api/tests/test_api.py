from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_predict_returns_probability():
    response = client.post("/predict", json={
        "x_coord": 58,
        "y_coord": -25,
        "shot_type": "wrist",
        "away_skaters": 5,
        "home_skaters": 5,
        "period": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert 0 <= data["goal_probability"] <= 1
    assert "is_high_danger" in data

def test_high_danger_shot():
    response = client.post("/predict", json={
        "x_coord": 85,
        "y_coord": 3,
        "shot_type": "tip-in",
        "away_skaters": 5,
        "home_skaters": 5,
        "period": 1
    })
    assert response.status_code == 200
    assert response.json()["is_high_danger"] == True