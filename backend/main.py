from fastapi import FastAPI

app = FastAPI(title="DecoRoute API")

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy"}