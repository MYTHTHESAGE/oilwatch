from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.services.db_service import init_db
from backend.routes import detection, history
import os

app = FastAPI(title="OilWatch API")

os.makedirs("backend/static/masks", exist_ok=True)
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(detection.router)
app.include_router(history.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
