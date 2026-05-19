#!/bin/bash

# Start Alloy in background
alloy run alloy-config.alloy &

# Start FastAPI
uvicorn app.main:app --host 0.0.0.0 --port $PORT