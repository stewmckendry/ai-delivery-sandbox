import pytest
from fastapi.testclient import TestClient
from project.app.main import app

@pytest.fixture
def client():
    return TestClient(app)