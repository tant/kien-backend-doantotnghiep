from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta

client = TestClient(app)

def test_create_soil_sample():
    response = client.post(
        "/soil/samples/",
        json={
            "description": "Cây cam số 1",
            "soil_moisture": 42.5
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["description"] == "Cây cam số 1"
    assert data["soil_moisture"] == 42.5
    assert "timestamp" in data

def test_create_soil_sample_with_timestamp():
    timestamp = datetime.utcnow().isoformat()
    response = client.post(
        "/soil/samples/with-timestamp/",
        json={
            "description": "Cây cam số 1",
            "soil_moisture": 45.2,
            "timestamp": timestamp
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["description"] == "Cây cam số 1"
    assert data["soil_moisture"] == 45.2
    assert data["timestamp"] == timestamp

def test_get_soil_samples():
    response = client.get("/soil/samples/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        sample = data[0]
        assert "id" in sample
        assert "description" in sample
        assert "soil_moisture" in sample
        assert "timestamp" in sample

def test_get_soil_samples_pagination():
    response = client.get("/soil/samples/?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 2

def test_get_soil_samples_by_description_last_week():
    description = "Cây cam số 1"
    response = client.get(f"/soil/samples/weekly/{description}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        sample = data[0]
        assert sample["description"] == description
        # Kiểm tra timestamp trong khoảng 1 tuần
        sample_time = datetime.fromisoformat(sample["timestamp"].replace('Z', '+00:00'))
        week_ago = datetime.utcnow() - timedelta(days=7)
        assert sample_time >= week_ago
