from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.services.db_service import get_db, Detection

router = APIRouter()

@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    detections = db.query(Detection).order_by(desc(Detection.created_at)).limit(50).all()
    return detections
