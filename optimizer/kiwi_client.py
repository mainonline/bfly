import requests
from typing import Optional


class KiwiClient:
    """Client for interacting with Kiwi Tequila API."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://tequila-api.kiwi.com"
        self.headers = {"apikey": api_key}
    
    def get_main_airport(self, city: str) -> dict:
        """
        Resolve city name to main airport IATA code.
        
        Args:
            city: City name (e.g., "London")
            
        Returns:
            dict with keys: iata_code, lat, lon, city_name
        """
        url = f"{self.base_url}/locations/query"
        params = {
            "term": city,
            "location_types": "airport",
            "active_only": "true",
            "sort": "-rank",
            "limit": 1
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        locations = data.get("locations", [])
        
        if not locations:
            raise ValueError(f"No airport found for city: {city}")
        
        airport = locations[0]
        return {
            "iata_code": airport["code"],
            "lat": airport["location"]["lat"],
            "lon": airport["location"]["lon"],
            "city_name": airport["name"]
        }
    
    def search_flights(
        self,
        from_airport: str,
        to_airport: str,
        date_from: str,
        date_to: str
    ) -> Optional[dict]:
        """
        Search for cheapest one-way flight.
        
        Args:
            from_airport: Departure IATA code
            to_airport: Arrival IATA code
            date_from: Date in dd/mm/yyyy format
            date_to: Date in dd/mm/yyyy format
            
        Returns:
            dict with flight data or None if no flights found
            Keys: price, flyFrom, flyTo, route (with lat/lon)
        """
        url = f"{self.base_url}/v2/search"
        params = {
            "fly_from": from_airport,
            "fly_to": to_airport,
            "date_from": date_from,
            "date_to": date_to,
            "flight_type": "oneway",
            "adults": 1,
            "curr": "USD",
            "locale": "en",
            "limit": 1,
            "sort": "price",
            "asc": 1
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        flights = data.get("data", [])
        
        if not flights:
            return None
        
        return flights[0]
