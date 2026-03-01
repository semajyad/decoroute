from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from database import engine, Base
from routers import auth, trips, dive_sites, transit


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="DecoRoute API",
    description="Enterprise-grade scuba diving trip planner with Safe Transit Engine",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(trips.router, prefix="/api/trips", tags=["trips"])
app.include_router(dive_sites.router, prefix="/api/dive-sites", tags=["dive sites"])
app.include_router(transit.router, prefix="/api/transit", tags=["transit"])


@app.get("/")
async def root():
    return {"message": "DecoRoute API - Safe Transit Engine Running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "decoroute-api"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
