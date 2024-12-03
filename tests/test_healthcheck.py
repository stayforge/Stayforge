from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_healthcheck():
    response = client.get("/api/healthcheck/")
    assert response.status_code == 200
    assert response.json() == "pong"

def test_healthcheck_info():
    response = client.get("/api/healthcheck/info/")
    assert response.status_code == 200
