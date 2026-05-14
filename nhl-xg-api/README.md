# NHL Expected Goals (xG) API

A REST API that predicts the probability of an NHL shot resulting in a goal using a trained XGBoost model.

**Live API:** https://nhl-shot-data-api.onrender.com/docs

## What is xG?
Expected Goals (xG) is a metric used by NHL teams to evaluate shot quality. A shot from the slot has a higher xG than a shot from the blue line, even if neither scores.

## Model
- **Algorithm:** XGBoost classifier
- **Training data:** 30,957 real NHL shots from the 2023-24 season via the NHL Stats API
- **ROC-AUC:** 0.7606 (NHL team models are typically 0.76–0.80)
- **Top features:** slot position, shot distance, power play situation

## API Endpoints

### `POST /predict`
Predict goal probability for a shot.

**Request:**
```json
{
  "x_coord": 85,
  "y_coord": 3,
  "shot_type": "tip-in",
  "away_skaters": 5,
  "home_skaters": 5,
  "period": 1
}
```

**Response:**
```json
{
  "goal_probability": 0.31,
  "is_high_danger": true,
  "distance": 12.4,
  "angle": 13.5,
  "model_version": "1.0.0"
}
```

### `GET /health`
Returns API status.

## Local Setup

```bash
git clone https://github.com/ap001AP/NHL-Shot-Data-API
cd NHL-Shot-Data-API/nhl-xg-api
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Docker

```bash
docker build -t nhl-xg-api .
docker run -p 8000:8000 nhl-xg-api
```

## Tech Stack
- **FastAPI** — REST API framework
- **XGBoost** — gradient boosted model
- **NHL Stats API** — real shot data, no third-party datasets
- **Docker** — containerized deployment
- **Render** — cloud deployment
