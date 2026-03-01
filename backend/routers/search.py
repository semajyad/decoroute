"""
🔍 SEARCH API ROUTES
API endpoints for dive trip pricing search using DuckDuckGo
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from search_service import search_dive_pricing, get_trip_cost_breakdown, search_service
except ImportError:
    # Fallback if search_service is not available
    search_service = None

router = APIRouter()


class PricingSearchRequest(BaseModel):
    location: str
    duration_days: int = 7


class MultipleLocationSearchRequest(BaseModel):
    locations: List[str]
    duration_days: int = 7


class PricingResponse(BaseModel):
    location: str
    duration_days: int
    pricing: dict
    location_info: dict
    data_source: str
    confidence: str
    search_metadata: Optional[dict] = None


@router.post("/pricing", response_model=PricingResponse)
async def search_trip_pricing(request: PricingSearchRequest):
    """
    Search for realistic dive trip pricing for a specific location
    
    Args:
        request: PricingSearchRequest with location and duration
        
    Returns:
        PricingResponse with detailed pricing information
    """
    try:
        if not search_service:
            # Fallback response if search service is not available
            return PricingResponse(
                location=request.location,
                duration_days=request.duration_days,
                pricing={
                    "average_price": 1500.0,
                    "min_price": 1000.0,
                    "max_price": 2500.0,
                    "budget_price": 1100.0,
                    "luxury_price": 2250.0,
                    "price_per_day": 1500.0 / request.duration_days,
                    "sample_prices": []
                },
                location_info={"note": "Search service unavailable - using estimates"},
                data_source="fallback",
                confidence="low"
            )
        
        # Search for pricing
        result = search_dive_pricing(request.location, request.duration_days)
        
        return PricingResponse(**result)
        
    except Exception as e:
        print(f"Error in pricing search: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )


@router.post("/pricing/breakdown", response_model=PricingResponse)
async def get_pricing_breakdown(request: PricingSearchRequest):
    """
    Get detailed pricing breakdown for trip components
    
    Args:
        request: PricingSearchRequest with location and duration
        
    Returns:
        PricingResponse with component breakdown
    """
    try:
        if not search_service:
            # Fallback response
            return PricingResponse(
                location=request.location,
                duration_days=request.duration_days,
                pricing={
                    "average_price": 1500.0,
                    "min_price": 1000.0,
                    "max_price": 2500.0,
                    "budget_price": 1100.0,
                    "luxury_price": 2250.0,
                    "price_per_day": 1500.0 / request.duration_days,
                    "components": {
                        "accommodation": {"percentage": 35, "estimated_cost": 525.0},
                        "diving": {"percentage": 25, "estimated_cost": 375.0},
                        "meals": {"percentage": 20, "estimated_cost": 300.0},
                        "transportation": {"percentage": 15, "estimated_cost": 225.0},
                        "equipment": {"percentage": 5, "estimated_cost": 75.0}
                    }
                },
                location_info={"note": "Search service unavailable - using estimates"},
                data_source="fallback",
                confidence="low"
            )
        
        # Get detailed breakdown
        result = get_trip_cost_breakdown(request.location, request.duration_days)
        
        return PricingResponse(**result)
        
    except Exception as e:
        print(f"Error in pricing breakdown: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Breakdown failed: {str(e)}"
        )


@router.post("/pricing/multiple", response_model=List[PricingResponse])
async def search_multiple_locations(request: MultipleLocationSearchRequest):
    """
    Search pricing for multiple locations
    
    Args:
        request: MultipleLocationSearchRequest with locations list
        
    Returns:
        List of PricingResponse for each location
    """
    try:
        if not search_service:
            # Fallback responses
            results = []
            for location in request.locations:
                results.append(PricingResponse(
                    location=location,
                    duration_days=request.duration_days,
                    pricing={
                        "average_price": 1500.0,
                        "min_price": 1000.0,
                        "max_price": 2500.0,
                        "budget_price": 1100.0,
                        "luxury_price": 2250.0,
                        "price_per_day": 1500.0 / request.duration_days,
                        "sample_prices": []
                    },
                    location_info={"note": "Search service unavailable - using estimates"},
                    data_source="fallback",
                    confidence="low"
                ))
            return results
        
        # Search multiple locations
        results = search_service.search_multiple_locations(request.locations, request.duration_days)
        
        return [PricingResponse(**result) for result in results]
        
    except Exception as e:
        print(f"Error in multiple location search: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Multiple search failed: {str(e)}"
        )


@router.get("/locations/popular")
async def get_popular_dive_locations():
    """
    Get list of popular dive locations for search suggestions
    
    Returns:
        List of popular dive locations
    """
    popular_locations = [
        {"name": "Belize", "description": "Great Blue Hole and barrier reef"},
        {"name": "Red Sea", "description": "Crystal clear waters and vibrant marine life"},
        {"name": "Great Barrier Reef", "description": "World's largest coral reef system"},
        {"name": "Maldives", "description": "Tropical paradise diving"},
        {"name": "Caribbean", "description": "Multiple island destinations"},
        {"name": "Thailand", "description": "Similan Islands and rich marine life"},
        {"name": "Indonesia", "description": "Bali and Komodo diving"},
        {"name": "Philippines", "description": "World-class macro diving"},
        {"name": "Hawaii", "description": "Volcanic reefs and marine life"},
        {"name": "Florida", "description": "Florida Keys and wrecks"},
        {"name": "Galapagos", "description": "Unique marine ecosystem"},
        {"name": "Palau", "description": "World-renowned dive sites"}
    ]
    
    return {"popular_locations": popular_locations}


@router.get("/search/health")
async def search_health_check():
    """
    Health check for search service
    
    Returns:
        Search service status
    """
    return {
        "status": "healthy",
        "service": "duckduckgo_search",
        "available": search_service is not None,
        "message": "Search service operational" if search_service else "Search service unavailable"
    }
