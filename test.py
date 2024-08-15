from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_status_counts():
    response = client.get("/status-counts/", params={"start_time": "2024-08-15T00:00:00", "end_time": "2024-08-15T23:59:59"})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
