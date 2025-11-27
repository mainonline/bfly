import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from api.index import app


client = TestClient(app)


@pytest.fixture
def mock_env_api_key(monkeypatch):
    """Mock KIWI_API_KEY environment variable."""
    monkeypatch.setenv("KIWI_API_KEY", "test_api_key")


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Flight Optimizer API"}


@patch("api.index.find_best_flight_per_km")
@patch("api.index.KiwiClient")
def test_optimize_success(mock_kiwi_client, mock_find_best, mock_env_api_key):
    mock_find_best.return_value = {
        "destination": "Paris",
        "price_per_km": 0.44,
        "price_usd": 150.0,
        "distance_km": 344.0,
        "airport_from": "LHR",
        "airport_to": "CDG",
    }

    response = client.post(
        "/optimize", json={"from_city": "London", "to_cities": ["Paris", "Berlin"]}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["destination"] == "Paris"
    assert data["price_per_km"] == 0.44
    assert data["price_usd"] == 150.0


@patch("api.index.find_best_flight_per_km")
@patch("api.index.KiwiClient")
def test_optimize_no_flights(mock_kiwi_client, mock_find_best, mock_env_api_key):
    mock_find_best.side_effect = ValueError("No flights available")

    response = client.post(
        "/optimize", json={"from_city": "London", "to_cities": ["Paris"]}
    )

    assert response.status_code == 400
    assert "No flights available" in response.json()["detail"]


def test_optimize_missing_api_key(monkeypatch):
    monkeypatch.delenv("KIWI_API_KEY", raising=False)

    response = client.post(
        "/optimize", json={"from_city": "London", "to_cities": ["Paris"]}
    )

    assert response.status_code == 500
    assert "API key not configured" in response.json()["detail"]


def test_optimize_invalid_request():
    response = client.post("/optimize", json={"from_city": "London"})

    assert response.status_code == 422
