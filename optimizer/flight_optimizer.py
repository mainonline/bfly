from datetime import datetime, timedelta
from typing import TypedDict, Optional
from geopy.distance import geodesic
from optimizer.kiwi_client import KiwiClient


class FlightResult(TypedDict):
    destination: str
    price_per_km: float
    price_usd: float
    distance_km: float
    airport_from: str
    airport_to: str


def calculate_distance(
    from_lat: float,
    from_lon: float,
    to_lat: float,
    to_lon: float
) -> float:
    """
    Calculate geodesic distance between two points.
    Returns distance in kilometers
    """
    return geodesic((from_lat, from_lon), (to_lat, to_lon)).km


def get_cheapest_flight(
    from_airport: dict,
    to_airport: dict,
    kiwi_client: KiwiClient
) -> Optional[dict]:
    """
    Find cheapest flight in next 24 hours.
    
    Args:
        from_airport: dict with iata_code, lat, lon
        to_airport: dict with iata_code, lat, lon
        kiwi_client: Kiwi API client instance
        
    Returns:
        dict with price, distance_km, or None if no flights
    """
    # Calculate date range (today and tomorrow in UTC)
    today = datetime.utcnow()
    tomorrow = today + timedelta(days=1)
    
    # Format dates as dd/mm/yyyy
    date_from = today.strftime("%d/%m/%Y")
    date_to = tomorrow.strftime("%d/%m/%Y")
    
    flight = kiwi_client.search_flights(
        from_airport["iata_code"],
        to_airport["iata_code"],
        date_from,
        date_to
    )
    
    if not flight:
        return None
    
    distance_km = calculate_distance(
        from_airport["lat"],
        from_airport["lon"],
        to_airport["lat"],
        to_airport["lon"]
    )
    
    return {
        "price": flight["price"],
        "distance_km": distance_km,
        "flyFrom": flight["flyFrom"],
        "flyTo": flight["flyTo"]
    }


def find_best_flight_per_km(
    from_city: str,
    to_cities: list[str],
    kiwi_client: KiwiClient
) -> FlightResult:
    """
    Find destination with lowest price per kilometer.
    
    Args:
        from_city: Departure city name
        to_cities: List of destination city names
        kiwi_client: Kiwi API client instance
        
    Returns:
        FlightResult with best destination and metrics
        
    Raises:
        ValueError: If no valid flights found to any destination
    """
    from_airport = kiwi_client.get_main_airport(from_city)
    
    # Evaluate each destination
    best_destination = None
    best_price_per_km = float('inf')
    best_flight_data = None
    
    # NOTE: we can use asyncio.gather for potential speedup
    for to_city in to_cities:
        try:
            to_airport = kiwi_client.get_main_airport(to_city)
            
            # Get cheapest flight
            flight_data = get_cheapest_flight(from_airport, to_airport, kiwi_client)
            
            if flight_data is None:
                continue
            
            # Handle zero or invalid distance
            if flight_data["distance_km"] <= 0:
                continue
            
            # Calculate price per kilometer
            price_per_km = flight_data["price"] / flight_data["distance_km"]
            
            # Check if this is the best option
            if price_per_km < best_price_per_km:
                best_price_per_km = price_per_km
                best_destination = to_city
                best_flight_data = flight_data
        
        except ValueError:
            # Invalid city, skip
            continue
    
    if best_destination is None or best_flight_data is None:
        raise ValueError("No flights available to any destination")
    
    return {
        "destination": best_destination,
        "price_per_km": round(best_price_per_km, 2),
        "price_usd": best_flight_data["price"],
        "distance_km": best_flight_data["distance_km"],
        "airport_from": best_flight_data["flyFrom"],
        "airport_to": best_flight_data["flyTo"]
    }
