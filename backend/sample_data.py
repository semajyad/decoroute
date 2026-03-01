"""
Sample data script for DecoRoute
Populates the database with sample dive sites and transit routes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import sessionmaker
from database import engine, Base
from models import DiveSite, TransitRoute
from datetime import datetime

def create_sample_data():
    """Create sample dive sites and transit routes"""
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Sample dive sites
        dive_sites = [
            DiveSite(
                name="Coral Bay",
                description="Beautiful coral reef with abundant marine life",
                location="Red Sea",
                country="Egypt",
                latitude=27.0,
                longitude=34.0,
                max_depth=25.0,
                water_type="saltwater",
                difficulty_level="intermediate",
                marine_life_highlights="Turtles, rays, colorful reef fish",
                best_season="Spring, Fall",
                certification_required="Open Water",
                average_visibility=30.0,
                current_strength="moderate",
                is_active=True
            ),
            DiveSite(
                name="Deep Wall",
                description="Advanced deep wall dive with pelagic encounters",
                location="Pacific Ocean",
                country="Philippines",
                latitude=10.0,
                longitude=124.0,
                max_depth=40.0,
                water_type="saltwater",
                difficulty_level="advanced",
                marine_life_highlights="Sharks, barracudas, tuna",
                best_season="Winter, Spring",
                certification_required="Advanced Open Water",
                average_visibility=25.0,
                current_strength="strong",
                is_active=True
            ),
            DiveSite(
                name="Wreck Explorer",
                description="Historic shipwreck in excellent condition",
                location="Caribbean Sea",
                country="Belize",
                latitude=16.5,
                longitude=-88.0,
                max_depth=35.0,
                water_type="saltwater",
                difficulty_level="advanced",
                marine_life_highlights="Wreck history, marine growth, groupers",
                best_season="Year-round",
                certification_required="Advanced Open Water",
                average_visibility=20.0,
                current_strength="light",
                is_active=True
            ),
            DiveSite(
                name="Shallow Reef",
                description="Perfect for beginners and photography",
                location="Indian Ocean",
                country="Maldives",
                latitude=3.0,
                longitude=73.0,
                max_depth=18.0,
                water_type="saltwater",
                difficulty_level="beginner",
                marine_life_highlights="Coral gardens, small fish, macro life",
                best_season="November - April",
                certification_required="Open Water",
                average_visibility=40.0,
                current_strength="light",
                is_active=True
            ),
            DiveSite(
                name="Cave System",
                description="Extensive underwater cave system",
                location="Freshwater",
                country="Mexico",
                latitude=20.0,
                longitude=-87.0,
                max_depth=30.0,
                water_type="freshwater",
                difficulty_level="advanced",
                marine_life_highlights="Stalactites, cavern formations",
                best_season="Year-round",
                certification_required="Cave Diver",
                average_visibility=50.0,
                current_strength="none",
                is_active=True
            )
        ]
        
        # Add dive sites
        for site in dive_sites:
            db.add(site)
        
        db.commit()
        
        # Refresh to get IDs
        for site in dive_sites:
            db.refresh(site)
        
        # Sample transit routes
        transit_routes = [
            TransitRoute(
                from_site_id=1,  # Coral Bay
                to_site_id=2,    # Deep Wall
                transport_type="flight",
                distance_km=8500,
                travel_time_hours=12,
                cost_estimate=800,
                departure_times="06:00, 14:00, 22:00",
                arrival_times="18:00+1, 02:00+1, 10:00+1",
                restrictions="No diving 24h before flight",
                is_active=True
            ),
            TransitRoute(
                from_site_id=2,    # Deep Wall
                to_site_id=3,      # Wreck Explorer
                transport_type="flight",
                distance_km=12000,
                travel_time_hours=16,
                cost_estimate=1200,
                departure_times="08:00, 20:00",
                arrival_times="00:00+1, 12:00+1",
                restrictions="No diving 24h before flight",
                is_active=True
            ),
            TransitRoute(
                from_site_id=3,    # Wreck Explorer
                to_site_id=4,      # Shallow Reef
                transport_type="flight",
                distance_km=15000,
                travel_time_hours=20,
                cost_estimate=1500,
                departure_times="10:00",
                arrival_times="06:00+1",
                restrictions="No diving 24h before flight",
                is_active=True
            ),
            TransitRoute(
                from_site_id=4,    # Shallow Reef
                to_site_id=5,      # Cave System
                transport_type="flight",
                distance_km=14000,
                travel_time_hours=18,
                cost_estimate=1300,
                departure_times="12:00, 23:00",
                arrival_times="06:00+1, 17:00+1",
                restrictions="No diving 24h before flight",
                is_active=True
            ),
            TransitRoute(
                from_site_id=1,    # Coral Bay
                to_site_id=3,      # Wreck Explorer
                transport_type="flight",
                distance_km=9000,
                travel_time_hours=14,
                cost_estimate=900,
                departure_times="07:00, 15:00",
                arrival_times="21:00, 05:00+1",
                restrictions="No diving 24h before flight",
                is_active=True
            ),
            TransitRoute(
                from_site_id=2,    # Deep Wall
                to_site_id=4,      # Shallow Reef
                transport_type="boat",
                distance_km=5000,
                travel_time_hours=8,
                cost_estimate=200,
                departure_times="06:00, 14:00",
                arrival_times="14:00, 22:00",
                restrictions="Weather dependent",
                is_active=True
            )
        ]
        
        # Add transit routes
        for route in transit_routes:
            db.add(route)
        
        db.commit()
        
        print("✓ Sample data created successfully!")
        print(f"✓ Created {len(dive_sites)} dive sites")
        print(f"✓ Created {len(transit_routes)} transit routes")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()
