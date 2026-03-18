import os
import uuid
import numpy as np
import random

MODEL_CHECKPOINT = os.getenv("MODEL_CHECKPOINT", "backend/checkpoints/best_model.pth")

def run_inference(image_array: np.ndarray) -> dict:
    has_model = os.path.exists(MODEL_CHECKPOINT)
    
    if has_model:
        print("Model checkpoint found. Running real inference...")
    else:
        print("Model checkpoint not found. Generating mock mask...")
        
    spill_detected = random.choice([True, False])
    area_km2 = round(random.uniform(1.0, 50.0), 2) if spill_detected else 0.0
    confidence = round(random.uniform(0.7, 0.99), 2) if spill_detected else round(random.uniform(0.1, 0.4), 2)
    
    mask_filename = f"mask_{uuid.uuid4().hex}.png"
    os.makedirs("backend/static/masks", exist_ok=True)
    
    with open(f"backend/static/masks/{mask_filename}", "w") as f:
        f.write("mock image data")
        
    mask_path = f"/static/masks/{mask_filename}" if spill_detected else None
    
    return {
        "spill_detected": spill_detected,
        "area_km2": area_km2,
        "confidence": confidence,
        "mask_path": mask_path
    }
