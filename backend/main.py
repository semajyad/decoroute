from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DecoRoute API")

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