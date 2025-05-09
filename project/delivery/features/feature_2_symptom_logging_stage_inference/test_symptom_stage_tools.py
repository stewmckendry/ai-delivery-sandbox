import pytest
from datetime import datetime, date
from fastapi.testclient import TestClient
from app.tools.symptom_logger import router as log_router
from app.tools.get_stage_guidance import router as stage_router
from app.models.symptoms import SymptomCheckIn, StageInferenceRequest
from app.models.tracker import TrackerState
from fastapi import FastAPI

# Setup app for testing
app = FastAPI()
app.include_router(log_router)
app.include_router(stage_router)
client = TestClient(app)

def test_log_symptoms_valid():
    payload = {
        "user_id": "test_user",
        "injury_date": str(date.today()),
        "checkin_time": datetime.now().isoformat(),
        "symptoms": {
            "drowsiness": 2,
            "headache": 3
        }
    }
    response = client.post("/log_symptoms", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "tracker_state" in data
    assert data["tracker_state"]["answers"] == payload["symptoms"]

def test_get_stage_guidance_valid():
    tracker_state = {
        "user_id": "test_user",
        "injury_date": str(date.today()),
        "checkin_time": datetime.now().isoformat(),
        "answers": {
            "drowsiness": 1,
            "headache": 2
        },
        "last_stage_id": "",
        "cleared_to_play": False
    }
    payload = {
        "user_id": "test_user",
        "tracker_state": tracker_state
    }
    response = client.post("/get_stage_guidance", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "stage_result" in data
    assert "message" in data