from fastapi import FastAPI
from app.schemas import ShotRequest, ShotResponse
from app.model import predict_xg
from prometheus_fastapi_instrumentator import Instrumentator
import threading
import time
import requests
from prometheus_client import CollectorRegistry, generate_latest, REGISTRY

app = FastAPI(
    title="NHL Expected Goals (xG) API",
    description="Predict the probability a shot results in a goal using a trained XGBoost model.",
    version="1.0.0",
)

Instrumentator().instrument(app).expose(app)

def push_metrics():
    import os
    import requests
    from prometheus_client import generate_latest, REGISTRY

    # InfluxDB line protocol endpoint — accepts plain text
    url = "https://prometheus-prod-32-prod-ca-east-0.grafana.net/api/v1/push/influx/write"
    username = "3222572"
    password = os.environ.get("GRAFANA_API_KEY", "")

    while True:
        try:
            # Convert prometheus metrics to influx line protocol
            lines = []
            from prometheus_client.parser import text_string_to_metric_families
            metrics_text = generate_latest(REGISTRY).decode("utf-8")
            
            for family in text_string_to_metric_families(metrics_text):
                for sample in family.samples:
                    tags = ",".join(f'{k}={v.replace(" ", "_")}' 
                                   for k, v in sample.labels.items() if v)
                    measurement = sample.name
                    if tags:
                        line = f"{measurement},{tags} value={sample.value}"
                    else:
                        line = f"{measurement} value={sample.value}"
                    lines.append(line)

            response = requests.post(
                url,
                data="\n".join(lines),
                headers={"Content-Type": "text/plain"},
                auth=(username, password),
                timeout=10,
            )
            if response.status_code not in (200, 204):
                print(f"Metrics push failed: {response.status_code} - {response.text[:150]}")
            else:
                print("Metrics pushed successfully")
        except Exception as e:
            print(f"Metrics push error: {e}")
        time.sleep(15)
        
@app.on_event("startup")
def start_metrics_pusher():
    if __import__("os").environ.get("GRAFANA_API_KEY"):
        thread = threading.Thread(target=push_metrics, daemon=True)
        thread.start()
        print("Metrics pusher started")


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