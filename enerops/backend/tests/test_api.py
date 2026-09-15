from fastapi.testclient import TestClient
from app.main import app

# ponytail: simple synchronous in-memory TestClient (no live server or async marks needed)
client = TestClient(app, headers={"Authorization": "Bearer MOCK_TOKEN_ADMIN"})

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}

def test_post_ai_chat():
    res = client.post("/v1/ai/chat", json={"message": "Anomaly"})
    assert res.status_code == 200
    data = res.json()
    assert "reply" in data

def test_get_ai_anomalies():
    res = client.get("/v1/ai/anomalies")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "severity" in data[0]

def test_get_ai_forecast():
    res = client.get("/v1/ai/forecast")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) == 12
    assert "predicted_kwh" in data[0]

def test_get_reports_list():
    res = client.get("/v1/reports/list")
    assert res.status_code == 200
    data = res.json()
    assert "reports" in data

