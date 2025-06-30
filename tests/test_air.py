from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta

client = TestClient(app)

def test_create_air_sample():
    response = client.post(
        "/air/samples/",
        json={
            "temperature": 25.6,
            "humidity": 65.4,
            "pressure": 1013.2
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["temperature"] == 25.6
    assert data["humidity"] == 65.4
    assert data["pressure"] == 1013.2
    assert "timestamp" in data

def test_create_air_sample_with_timestamp():
    timestamp = datetime.utcnow().isoformat()
    response = client.post(
        "/air/samples/with-timestamp/",
        json={
            "temperature": 26.5,
            "humidity": 70.2,
            "pressure": 1012.8,
            "timestamp": timestamp
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["temperature"] == 26.5
    assert data["humidity"] == 70.2
    assert data["pressure"] == 1012.8
    assert data["timestamp"] == timestamp

def test_get_air_samples():
    response = client.get("/air/samples/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        sample = data[0]
        assert "id" in sample
        assert "temperature" in sample
        assert "humidity" in sample
        assert "pressure" in sample
        assert "timestamp" in sample

def test_get_air_samples_pagination():
    # Test với limit và skip
    response = client.get("/air/samples/?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 2  # Số lượng kết quả không vượt quá limit

def test_get_air_samples_last_week():
    response = client.get("/air/samples/weekly/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        sample = data[0]
        assert "id" in sample
        # Kiểm tra timestamp trong khoảng 1 tuần
        sample_time = datetime.fromisoformat(sample["timestamp"].replace('Z', '+00:00'))
        week_ago = datetime.utcnow() - timedelta(days=7)
        assert sample_time >= week_ago
