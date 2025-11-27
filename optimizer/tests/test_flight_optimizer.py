import pytest
from unittest.mock import Mock
from optimizer.flight_optimizer import calculate_distance, find_best_flight_per_km
from optimizer.kiwi_client import KiwiClient


def test_calculate_distance():
    london_lat, london_lon = 51.4700, -0.4543
    paris_lat, paris_lon = 49.0097, 2.5479
    
    distance = calculate_distance(london_lat, london_lon, paris_lat, paris_lon)
    
    assert 334 <= distance <= 354


def test_find_best_flight_per_km():
    """Test finding cheapest destination by price per km."""
    mock_client = Mock(spec=KiwiClient)
    
    airports = {
        "London": {"iata_code": "LHR", "lat": 51.47, "lon": -0.45},
        "Paris": {"iata_code": "CDG", "lat": 49.01, "lon": 2.55},
        "Berlin": {"iata_code": "TXL", "lat": 52.56, "lon": 13.29}
    }
    
    flights = {
        ("LHR", "CDG"): {"price": 150.0, "flyFrom": "LHR", "flyTo": "CDG"},
        ("LHR", "TXL"): {"price": 200.0, "flyFrom": "LHR", "flyTo": "TXL"}
    }
    
    mock_client.get_main_airport.side_effect = lambda city: airports[city]
    mock_client.search_flights.side_effect = lambda f, t, *_: flights.get((f, t))
    
    result = find_best_flight_per_km("London", ["Paris", "Berlin"], mock_client)
    
    assert result["destination"] in ["Paris", "Berlin"]
    assert result["price_per_km"] > 0
    assert result["price_usd"] > 0
    assert result["distance_km"] > 0


def test_no_flights_available():
    """Test error when no flights exist to any destination."""
    mock_client = Mock(spec=KiwiClient)
    
    mock_client.get_main_airport.return_value = {"iata_code": "LHR", "lat": 51.47, "lon": -0.45}
    mock_client.search_flights.return_value = None
    
    with pytest.raises(ValueError, match="No flights available"):
        find_best_flight_per_km("London", ["Paris"], mock_client)
