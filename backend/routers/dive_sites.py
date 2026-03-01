from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
import random
from datetime import datetime

from database import get_db
from models import DiveSite

router = APIRouter()


class DiveSiteResponse(BaseModel):
    id: int
    name: str
    description: str
    location: str
    country: str
    latitude: float
    longitude: float
    max_depth: float
    water_type: str
    difficulty_level: str
    marine_life_highlights: str
    best_season: str
    certification_required: str
    average_visibility: float
    current_strength: str

    class Config:
        from_attributes = True


def get_demo_dive_sites() -> List[dict]:
    """Get demo dive sites for fallback scenarios"""
    return [
        {
            "id": 1,
            "name": "Coral Bay",
            "description": "Beautiful coral reef with abundant marine life",
            "location": "Red Sea",
            "country": "Egypt",
            "latitude": 27.0,
            "longitude": 34.0,
            "max_depth": 30.0,
            "water_type": "saltwater",
            "difficulty_level": "intermediate",
            "marine_life_highlights": "Coral, tropical fish, turtles",
            "best_season": "Year-round",
            "certification_required": "Open Water",
            "average_visibility": 20.0,
            "current_strength": "moderate"
        },
        {
            "id": 2,
            "name": "Blue Hole",
            "description": "Deep blue hole dive adventure",
            "location": "Belize Barrier Reef",
            "country": "Belize",
            "latitude": 17.0,
            "longitude": -88.0,
            "max_depth": 40.0,
            "water_type": "saltwater",
            "difficulty_level": "advanced",
            "marine_life_highlights": "Deep water species, sharks",
            "best_season": "Apr-Jun",
            "certification_required": "Advanced",
            "average_visibility": 30.0,
            "current_strength": "strong"
        },
        {
            "id": 3,
            "name": "Great Barrier Reef",
            "description": "World's largest coral reef system",
            "location": "Queensland",
            "country": "Australia",
            "latitude": -18.0,
            "longitude": 147.0,
            "max_depth": 25.0,
            "water_type": "saltwater",
            "difficulty_level": "intermediate",
            "marine_life_highlights": "Coral, rays, sharks",
            "best_season": "Sep-Nov",
            "certification_required": "Open Water",
            "average_visibility": 15.0,
            "current_strength": "moderate"
        },
        {
            "id": 4,
            "name": "Red Sea",
            "description": "Crystal clear waters and vibrant marine life",
            "location": "Hurghada",
            "country": "Egypt",
            "latitude": 27.0,
            "longitude": 33.0,
            "max_depth": 35.0,
            "water_type": "saltwater",
            "difficulty_level": "intermediate",
            "marine_life_highlights": "Coral, dolphins",
            "best_season": "Year-round",
            "certification_required": "Open Water",
            "average_visibility": 25.0,
            "current_strength": "moderate"
        },
        {
            "id": 5,
            "name": "Maldives",
            "description": "Tropical paradise diving experience",
            "location": "North Male Atoll",
            "country": "Maldives",
            "latitude": 4.0,
            "longitude": 73.0,
            "max_depth": 20.0,
            "water_type": "saltwater",
            "difficulty_level": "beginner",
            "marine_life_highlights": "Manta rays, whale sharks",
            "best_season": "Dec-May",
            "certification_required": "Open Water",
            "average_visibility": 30.0,
            "current_strength": "mild"
        }
    ]


@router.get("/", response_model=List[DiveSiteResponse])
async def get_dive_sites(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        sites = db.query(DiveSite).filter(DiveSite.is_active == True).offset(skip).limit(limit).all()
        return sites
    except Exception as e:
        print(f"Database error in get_dive_sites: {e}")
        # Fallback to demo mode
        demo_sites = get_demo_dive_sites()
        return [DiveSiteResponse(**site) for site in demo_sites[skip:skip+limit]]


@router.get("/{site_id}", response_model=DiveSiteResponse)
async def get_dive_site(site_id: int, db: Session = Depends(get_db)):
    try:
        site = db.query(DiveSite).filter(DiveSite.id == site_id, DiveSite.is_active == True).first()
        if not site:
            raise HTTPException(status_code=404, detail="Dive site not found")
        return site
    except HTTPException:
        raise
    except Exception as e:
        print(f"Database error in get_dive_site: {e}")
        # Fallback to demo mode
        demo_sites = get_demo_dive_sites()
        for site in demo_sites:
            if site["id"] == site_id:
                return DiveSiteResponse(**site)
        # If not found, return first site
        return DiveSiteResponse(**demo_sites[0])


@router.get("/search/{query}", response_model=List[DiveSiteResponse])
async def search_dive_sites(query: str, db: Session = Depends(get_db)):
    try:
        sites = db.query(DiveSite).filter(
            DiveSite.is_active == True,
            DiveSite.name.ilike(f"%{query}%")
        ).limit(20).all()
        return sites
    except Exception as e:
        print(f"Database error in search_dive_sites: {e}")
        # Fallback to demo mode
        demo_sites = get_demo_dive_sites()
        filtered_sites = [site for site in demo_sites if query.lower() in site["name"].lower()]
        return [DiveSiteResponse(**site) for site in filtered_sites[:20]]
