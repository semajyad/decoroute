from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

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


@router.get("/", response_model=List[DiveSiteResponse])
async def get_dive_sites(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sites = db.query(DiveSite).filter(DiveSite.is_active == True).offset(skip).limit(limit).all()
    return sites


@router.get("/{site_id}", response_model=DiveSiteResponse)
async def get_dive_site(site_id: int, db: Session = Depends(get_db)):
    site = db.query(DiveSite).filter(DiveSite.id == site_id, DiveSite.is_active == True).first()
    if not site:
        raise HTTPException(status_code=404, detail="Dive site not found")
    return site


@router.get("/search/{query}", response_model=List[DiveSiteResponse])
async def search_dive_sites(query: str, db: Session = Depends(get_db)):
    sites = db.query(DiveSite).filter(
        DiveSite.is_active == True,
        DiveSite.name.ilike(f"%{query}%")
    ).limit(20).all()
    return sites
