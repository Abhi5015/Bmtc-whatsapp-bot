"""
Demo Transit Provider
Uses mock data for demonstration purposes
Replace with actual API integration (Tummoc, Moovit, etc.) when available
"""
import logging
from typing import List, Optional
from datetime import datetime, timedelta
from .provider import TransitProvider, BusArrival, RouteInfo, FareInfo

logger = logging.getLogger(__name__)

class DemoTransitProvider(TransitProvider):
    """Demo provider with mock BMTC data"""
    
    def __init__(self):
        # Mock database of routes
        self.routes = {
            "335E": RouteInfo(
                route_number="335E",
                origin="Kengeri Bus Terminal",
                destination="Kadugodi",
                stops=["Kengeri", "Vijayanagar", "Majestic", "Shivajinagar", "Indiranagar", "Kadugodi"],
                frequency_minutes=15
            ),
            "G-4": RouteInfo(
                route_number="G-4",
                origin="Banashankari",
                destination="Hebbal",
                stops=["Banashankari", "Jayanagar", "Majestic", "Yeshwanthpur", "Hebbal"],
                frequency_minutes=20
            ),
            "500K": RouteInfo(
                route_number="500K",
                origin="Kempegowda Bus Station",
                destination="Hosur Road",
                stops=["Majestic", "Corporation", "Shantinagar", "BTM Layout", "Hosur Road"],
                frequency_minutes=12
            ),
            "215Y": RouteInfo(
                route_number="215Y",
                origin="Yehalanka",
                destination="Silkboard",
                stops=["Yehalanka", "Hebbal", "Mekhri Circle", "Majestic", "Silkboard"],
                frequency_minutes=18
            ),
        }
        
        # Mock stop to routes mapping
        self.stop_routes = {
            "Majestic": ["335E", "G-4", "500K", "215Y"],
            "BTM Layout": ["500K", "335E"],
            "Silk Board": ["215Y", "335E"],
            "Hebbal": ["G-4", "215Y"],
            "Indiranagar": ["335E"],
        }
        
        logger.info("Demo Transit Provider initialized with mock data")
    
    def get_arrivals(self, stop_name: str) -> List[BusArrival]:
        """Get mock bus arrivals"""
        # Normalize stop name
        stop_name = self._normalize_stop_name(stop_name)
        
        if stop_name not in self.stop_routes:
            logger.warning(f"Stop not found: {stop_name}")
            return []
        
        arrivals = []
        base_time = datetime.now()
        
        for i, route_num in enumerate(self.stop_routes[stop_name][:3]):  # Return max 3
            route = self.routes.get(route_num)
            if route:
                eta_minutes = 4 + (i * 5)  # Mock: 4, 9, 14 minutes
                arrival = BusArrival(
                    route_number=route.route_number,
                    destination=route.destination,
                    eta_minutes=eta_minutes,
                    eta_timestamp=base_time + timedelta(minutes=eta_minutes)
                )
                arrivals.append(arrival)
        
        logger.info(f"Found {len(arrivals)} arrivals for {stop_name}")
        return arrivals
    
    def get_route_info(self, route_number: str) -> Optional[RouteInfo]:
        """Get route information"""
        route_number = route_number.upper().strip()
        route = self.routes.get(route_number)
        
        if route:
            logger.info(f"Found route info for {route_number}")
        else:
            logger.warning(f"Route not found: {route_number}")
        
        return route
    
    def get_fare(self, from_stop: str, to_stop: str) -> Optional[FareInfo]:
        """Calculate mock fare"""
        from_stop = self._normalize_stop_name(from_stop)
        to_stop = self._normalize_stop_name(to_stop)
        
        # Simple mock fare calculation
        base_fare = 10.0
        per_stop_fare = 5.0
        
        # Mock distance calculation
        mock_distance = 8.5
        fare = base_fare + per_stop_fare
        
        return FareInfo(
            from_stop=from_stop,
            to_stop=to_stop,
            fare_inr=fare,
            distance_km=mock_distance
        )
    
    def search_stops(self, query: str) -> List[str]:
        """Search for stops"""
        query = query.lower()
        matches = [
            stop for stop in self.stop_routes.keys()
            if query in stop.lower()
        ]
        return matches[:5]  # Return max 5 matches
    
    def _normalize_stop_name(self, stop_name: str) -> str:
        """Normalize stop name for matching"""
        # Simple normalization - map common variations
        stop_map = {
            "majestic": "Majestic",
            "kbs": "Majestic",
            "btm": "BTM Layout",
            "silkboard": "Silk Board",
            "silk board": "Silk Board",
        }
        
        normalized = stop_name.strip().lower()
        return stop_map.get(normalized, stop_name.title())

# Initialize global provider
transit_provider = DemoTransitProvider()
