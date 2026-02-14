"""
Transit Provider Interface
Abstraction layer for different transit data providers
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class BusArrival:
    """Bus arrival information"""
    route_number: str
    destination: str
    eta_minutes: int
    eta_timestamp: datetime
    
@dataclass
class RouteInfo:
    """Bus route information"""
    route_number: str
    origin: str
    destination: str
    stops: List[str]
    frequency_minutes: Optional[int] = None

@dataclass
class FareInfo:
    """Fare information"""
    from_stop: str
    to_stop: str
    fare_inr: float
    distance_km: Optional[float] = None

class TransitProvider(ABC):
    """Abstract base class for transit data providers"""
    
    @abstractmethod
    def get_arrivals(self, stop_name: str) -> List[BusArrival]:
        """Get upcoming bus arrivals at a stop"""
        pass
    
    @abstractmethod
    def get_route_info(self, route_number: str) -> Optional[RouteInfo]:
        """Get information about a specific route"""
        pass
    
    @abstractmethod
    def get_fare(self, from_stop: str, to_stop: str) -> Optional[FareInfo]:
        """Get fare between two stops"""
        pass
    
    @abstractmethod
    def search_stops(self, query: str) -> List[str]:
        """Search for stops by name"""
        pass
