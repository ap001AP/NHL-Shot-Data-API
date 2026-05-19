#!/bin/bash
alloy run alloy-config.alloy &
uvicorn app.main:app --host 0.0.0.0 --port $PORT