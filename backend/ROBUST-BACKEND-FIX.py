# 🔧 COMPREHENSIVE BACKEND FIXES
# This file contains all the fixes needed for robust error handling

import hashlib
import random
from datetime import datetime
from typing import List, Dict, Any

# Database fallback data
DEMO_DIVE_SITES = [
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
        "current_strength": "moderate",
        "is_active": True,
        "created_at": datetime.now()
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
        "current_strength": "strong",
        "is_active": True,
        "created_at": datetime.now()
    }
]

def create_demo_user(email: str, username: str, full_name: str, certification_level: str = "Open Water") -> Dict[str, Any]:
    """Create a demo user for fallback scenarios"""
    return {
        "id": random.randint(1000, 9999),
        "email": email,
        "username": username,
        "full_name": full_name,
        "certification_level": certification_level,
        "total_dives": 0,
        "created_at": datetime.now(),
        "is_active": True
    }

def create_demo_trip(name: str, description: str, user_id: int) -> Dict[str, Any]:
    """Create a demo trip for fallback scenarios"""
    return {
        "id": random.randint(1000, 9999),
        "name": name,
        "description": description,
        "start_date": datetime.now(),
        "end_date": datetime.now(),
        "total_cost_estimate": 1500.0,
        "status": "planned",
        "is_public": False,
        "user_id": user_id,
        "created_at": datetime.now()
    }

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

# Database initialization check
def initialize_database_if_needed():
    """Check if database tables exist and create them if needed"""
    try:
        from database import engine, Base
        from models import User, DiveSite, TransitRoute, SavedTrip
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Add sample dive sites if table is empty
        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()
        
        try:
            # Check if dive sites exist
            if db.query(DiveSite).count() == 0:
                # Add demo dive sites
                for site_data in DEMO_DIVE_SITES:
                    site = DiveSite(**site_data)
                    db.add(site)
                db.commit()
                print("✅ Database initialized with demo data")
            else:
                print("✅ Database already has data")
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("🔄 Using demo mode fallback")

# Robust error handling decorator
def handle_database_errors(fallback_func=None):
    """Decorator to handle database errors gracefully"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                print(f"❌ Database error in {func.__name__}: {e}")
                if fallback_func:
                    return await fallback_func(*args, **kwargs)
                else:
                    # Return a safe default response
                    return {"message": "Service temporarily unavailable", "status": "demo_mode"}
        return wrapper
    return decorator

print("🔧 Robust backend fixes loaded successfully!")
