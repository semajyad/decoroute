from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from pydantic import BaseModel

from database import get_db
from models import DiveSite, TransitRoute
from routers.auth import get_current_user

router = APIRouter()


class DivePlan(BaseModel):
    dive_site_id: int
    dive_datetime: datetime
    max_depth: float
    bottom_time: int


class TransitRequest(BaseModel):
    dives: List[DivePlan]
    flight_datetime: datetime


class TransitResponse(BaseModel):
    is_safe: bool
    violation_type: str
    recommended_wait_time: int
    details: str


@router.post("/check-safety", response_model=TransitResponse)
async def check_transit_safety(request: TransitRequest, db: Session = Depends(get_db)):
    """
    Safe Transit Engine - Calculates if transit violates no-fly rules
    Returns safety assessment based on dive profiles and flight time
    """
    
    if not request.dives:
        return TransitResponse(
            is_safe=True,
            violation_type="none",
            recommended_wait_time=0,
            details="No dives planned, transit is safe"
        )
    
    # Sort dives by datetime to find the most recent
    sorted_dives = sorted(request.dives, key=lambda x: x.dive_datetime, reverse=True)
    last_dive = sorted_dives[0]
    
    # Calculate time between last dive and flight
    time_diff = request.flight_datetime - last_dive.dive_datetime
    hours_since_last_dive = time_diff.total_seconds() / 3600
    
    # Apply dive safety rules
    # 18-hour rule for single dives, 24-hour for multiple dives or deep dives
    no_fly_hours = 18
    
    # Check if multiple dives in last 24 hours
    dives_24h = [dive for dive in request.dives if 
                 (last_dive.dive_datetime - dive.dive_datetime).total_seconds() <= 86400]
    
    # Check if any dive exceeds decompression limits
    deep_dive_threshold = 30  # meters
    has_deep_dive = any(dive.max_depth > deep_dive_threshold for dive in dives_24h)
    
    # Apply stricter rules for multiple dives or deep dives
    if len(dives_24h) > 1 or has_deep_dive:
        no_fly_hours = 24
    
    # Calculate recommended wait time
    recommended_wait = max(0, no_fly_hours - hours_since_last_dive)
    
    # Determine safety
    is_safe = hours_since_last_dive >= no_fly_hours
    
    violation_type = "none"
    details = ""
    
    if not is_safe:
        if len(dives_24h) > 1:
            violation_type = "multi_dive_24h_rule"
            details = f"Multiple dives in 24 hours require {no_fly_hours}h surface interval. Current: {hours_since_last_dive:.1f}h"
        elif has_deep_dive:
            violation_type = "deep_dive_24h_rule"
            details = f"Deep dive (>30m) requires {no_fly_hours}h surface interval. Current: {hours_since_last_dive:.1f}h"
        else:
            violation_type = "single_dive_18h_rule"
            details = f"Single dive requires {no_fly_hours}h surface interval. Current: {hours_since_last_dive:.1f}h"
    else:
        details = f"Safe for flight. Surface interval: {hours_since_last_dive:.1f}h (required: {no_fly_hours}h)"
    
    return TransitResponse(
        is_safe=is_safe,
        violation_type=violation_type,
        recommended_wait_time=int(recommended_wait),
        details=details
    )


@router.get("/routes/{from_site_id}/{to_site_id}")
async def get_transit_routes(from_site_id: int, to_site_id: int, db: Session = Depends(get_db)):
    routes = db.query(TransitRoute).filter(
        TransitRoute.from_site_id == from_site_id,
        TransitRoute.to_site_id == to_site_id,
        TransitRoute.is_active == True
    ).all()
    
    if not routes:
        raise HTTPException(status_code=404, detail="No transit routes found between these sites")
    
    return routes
