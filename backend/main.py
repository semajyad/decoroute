from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DecoRoute API")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables if they don't exist"""
    try:
        from database import engine, Base
        from models import User, DiveSite, TransitRoute, SavedTrip
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables initialized successfully")
        
        # Add sample data if needed
        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()
        
        try:
            # Add demo dive sites if table is empty
            from models import DiveSite
            if db.query(DiveSite).count() == 0:
                demo_sites = [
                    DiveSite(
                        name="Coral Bay",
                        description="Beautiful coral reef with abundant marine life",
                        location="Red Sea",
                        country="Egypt",
                        latitude=27.0,
                        longitude=34.0,
                        max_depth=30.0,
                        water_type="saltwater",
                        difficulty_level="intermediate",
                        marine_life_highlights="Coral, tropical fish, turtles",
                        best_season="Year-round",
                        certification_required="Open Water",
                        average_visibility=20.0,
                        current_strength="moderate",
                        is_active=True
                    ),
                    DiveSite(
                        name="Blue Hole",
                        description="Deep blue hole dive adventure",
                        location="Belize Barrier Reef",
                        country="Belize",
                        latitude=17.0,
                        longitude=-88.0,
                        max_depth=40.0,
                        water_type="saltwater",
                        difficulty_level="advanced",
                        marine_life_highlights="Deep water species, sharks",
                        best_season="Apr-Jun",
                        certification_required="Advanced",
                        average_visibility=30.0,
                        current_strength="strong",
                        is_active=True
                    )
                ]
                
                for site in demo_sites:
                    db.add(site)
                db.commit()
                print("✅ Demo dive sites added successfully")
            else:
                print("✅ Dive sites already exist")
                
        except Exception as e:
            print(f"❌ Error adding demo data: {e}")
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("🔄 Application will run in demo mode")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://semajyad.github.io", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "DecoRoute API - Safe Transit Engine Running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "decoroute-api"}

# Include routers
from routers import auth, trips, dive_sites, transit

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(trips.router, prefix="/api/trips", tags=["trips"])
app.include_router(dive_sites.router, prefix="/api/dive-sites", tags=["dive sites"])
app.include_router(transit.router, prefix="/api/transit", tags=["transit"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)