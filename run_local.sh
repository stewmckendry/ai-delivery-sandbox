#!/bin/bash
# Run the FastAPI app locally with autoreload.
PORT=${PORT:-8000}
exec uvicorn app.main:app --reload --host 0.0.0.0 --port "$PORT"
