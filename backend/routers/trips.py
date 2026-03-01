from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from models import User, SavedTrip, TripDive, TransitPlan
from routers.auth import get_current_user

router = APIRouter()


class TripCreate(BaseModel):
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    is_public: bool = False


class TripResponse(BaseModel):
    id: int
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    total_cost_estimate: float
    status: str
    is_public: bool
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("/", response_model=TripResponse)
async def create_trip(trip: TripCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_trip = SavedTrip(
        user_id=current_user.id,
        name=trip.name,
        description=trip.description,
        start_date=trip.start_date,
        end_date=trip.end_date,
        is_public=trip.is_public
    )
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip


@router.get("/", response_model=List[TripResponse])
async def get_user_trips(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    trips = db.query(SavedTrip).filter(SavedTrip.user_id == current_user.id).all()
    return trips


@router.get("/{trip_id}", response_model=TripResponse)
async def get_trip(trip_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    trip = db.query(SavedTrip).filter(
        SavedTrip.id == trip_id,
        SavedTrip.user_id == current_user.id
    ).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.delete("/{trip_id}")
async def delete_trip(trip_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    trip = db.query(SavedTrip).filter(
        SavedTrip.id == trip_id,
        SavedTrip.user_id == current_user.id
    ).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    db.delete(trip)
    db.commit()
    return {"message": "Trip deleted successfully"}
