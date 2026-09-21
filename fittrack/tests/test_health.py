"""
tests/test_health.py

Basic smoke test for Step 1: confirms the FastAPI app boots and the
/api/health endpoint responds correctly. Run with:

    pytest
"""

from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["application"] == "FitTrack"


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["application"] == "FitTrack"