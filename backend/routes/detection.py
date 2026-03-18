from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import date
from backend.services.db_service import get_db, Detection
from backend.services import gee_service, inference

router = APIRouter()

class DetectionRequest(BaseModel):
    bbox: list[float]
    start_date: str
    end_date: str

@router.post("/detect")
async def detect_spill(request: DetectionRequest, db: Session = Depends(get_db)):
    image_array = gee_service.fetch_sar_imagery(request.bbox, request.start_date, request.end_date)
    result = inference.run_inference(image_array)
    
    new_detection = Detection(
        bbox=request.bbox,
        start_date=date.fromisoformat(request.start_date),
        end_date=date.fromisoformat(request.end_date),
        spill_detected=result["spill_detected"],
        area_km2=result["area_km2"],
        confidence=result["confidence"],
        mask_path=result["mask_path"]
    )
    db.add(new_detection)
    db.commit()
    db.refresh(new_detection)
    
    return {
        "id": new_detection.id,
        "spill_detected": new_detection.spill_detected,
        "area_km2": new_detection.area_km2,
        "confidence": new_detection.confidence,
        "mask_path": new_detection.mask_path,
        "timestamp": new_detection.created_at
    }
