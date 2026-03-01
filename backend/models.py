from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    certification_level = Column(String, default="Open Water")
    total_dives = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    saved_trips = relationship("SavedTrip", back_populates="user")


class DiveSite(Base):
    __tablename__ = "dive_sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    location = Column(String, nullable=False)
    country = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    max_depth = Column(Float)
    water_type = Column(String, default="saltwater")
    difficulty_level = Column(String, default="intermediate")
    marine_life_highlights = Column(Text)
    best_season = Column(String)
    certification_required = Column(String, default="Open Water")
    average_visibility = Column(Float)
    current_strength = Column(String, default="moderate")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    transit_routes_from = relationship("TransitRoute", foreign_keys="TransitRoute.from_site_id", back_populates="from_site")
    transit_routes_to = relationship("TransitRoute", foreign_keys="TransitRoute.to_site_id", back_populates="to_site")


class TransitRoute(Base):
    __tablename__ = "transit_routes"

    id = Column(Integer, primary_key=True, index=True)
    from_site_id = Column(Integer, ForeignKey("dive_sites.id"), nullable=False)
    to_site_id = Column(Integer, ForeignKey("dive_sites.id"), nullable=False)
    transport_type = Column(String, nullable=False)
    distance_km = Column(Float)
    travel_time_hours = Column(Float, nullable=False)
    cost_estimate = Column(Float)
    departure_times = Column(Text)
    arrival_times = Column(Text)
    restrictions = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    from_site = relationship("DiveSite", foreign_keys=[from_site_id], back_populates="transit_routes_from")
    to_site = relationship("DiveSite", foreign_keys=[to_site_id], back_populates="transit_routes_to")


class SavedTrip(Base):
    __tablename__ = "saved_trips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    total_cost_estimate = Column(Float)
    status = Column(String, default="planned")
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="saved_trips")
    trip_dives = relationship("TripDive", back_populates="trip")
    transit_plans = relationship("TransitPlan", back_populates="trip")


class TripDive(Base):
    __tablename__ = "trip_dives"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("saved_trips.id"), nullable=False)
    dive_site_id = Column(Integer, ForeignKey("dive_sites.id"), nullable=False)
    dive_date = Column(DateTime(timezone=True), nullable=False)
    dive_time = Column(Time, nullable=False)
    max_depth_planned = Column(Float)
    bottom_time_planned = Column(Integer)
    dive_type = Column(String, default="recreational")
    equipment_needed = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    trip = relationship("SavedTrip", back_populates="trip_dives")
    dive_site = relationship("DiveSite")


class TransitPlan(Base):
    __tablename__ = "transit_plans"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("saved_trips.id"), nullable=False)
    transit_route_id = Column(Integer, ForeignKey("transit_routes.id"), nullable=False)
    planned_departure = Column(DateTime(timezone=True), nullable=False)
    planned_arrival = Column(DateTime(timezone=True), nullable=False)
    booking_reference = Column(String)
    cost_actual = Column(Float)
    status = Column(String, default="planned")
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    trip = relationship("SavedTrip", back_populates="transit_plans")
    transit_route = relationship("TransitRoute")
