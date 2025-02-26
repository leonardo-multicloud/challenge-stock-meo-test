import pytest
from api_backend.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    return client

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}

def test_get_available_currencies_unauthorized(client, monkeypatch):
    monkeypatch.setattr("api_backend.main.validate_api_key", lambda: True)
        
    response = client.get("/price/available")
    assert response.status_code == 200

def test_get_currency_status_unauthorized(client, monkeypatch):
    monkeypatch.setattr("api_backend.main.validate_api_key", lambda: True)
        
    response = client.get("/price/stats/USD")
    assert response.status_code == 200
