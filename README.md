# NHL Expected Goals (xG) API

A REST API that predicts the probability of an NHL shot resulting in a goal using a trained XGBoost model — with a full CI/CD pipeline and live monitoring dashboard.

## Live Links
- **API Docs:** https://nhl-shot-data-api.onrender.com/docs
- **CI/CD Pipeline:** https://github.com/ap001AP/NHL-Shot-Data-API/actions
- **Monitoring Dashboard:** https://ap001ap.grafana.net/public-dashboards/bc6df3331ccf41a19a68442147b28f67

## What is xG?
Expected Goals (xG) is a metric used by NHL teams to evaluate shot quality. A shot from the slot has a higher xG than a shot from the blue line, even if neither scores.

## Model
- **Algorithm:** XGBoost classifier
- **Training data:** 30,957 real NHL shots from the 2023-24 season via the NHL Stats API
- **ROC-AUC:** 0.7606 (NHL team models are typically 0.76–0.80)
- **Top features:** slot position, shot distance, power play situation

## Example
| Shot | Goal Probability |
|---|---|
| Tip-in from the slot, power play | 78% |
| Wrist shot from the right circle | 19% |
| Slap shot from the blue line | 13% |

## API Endpoints

### `POST /predict`
Predict goal probability for a shot.

**Request:**
```json
{
  "x_coord": 85,
  "y_coord": 3,
  "shot_type": "tip-in",
  "away_skaters": 4,
  "home_skaters": 5,
  "period": 2
}
```

**Response:**
```json
{
  "goal_probability": 0.78,
  "is_high_danger": true,
  "distance": 5.0,
  "angle": 36.87,
  "model_version": "1.0.0"
}
```

### `GET /health`
Returns API status.

### `GET /metrics`
Returns live Prometheus metrics pushed to Grafana Cloud every 15 seconds.

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
docker run -p 8000:8000 -e PORT=8000 nhl-xg-api
```

## Tech Stack
- **FastAPI** — REST API framework
- **XGBoost** — gradient boosted model
- **NHL Stats API** — real shot data, no third-party datasets
- **Docker** — containerized deployment
- **GitHub Actions** — CI/CD pipeline (test → build → push → deploy)
- **Prometheus** — API metrics instrumentation
- **Grafana Cloud** — live public monitoring dashboard
- **Render** — cloud deployment
