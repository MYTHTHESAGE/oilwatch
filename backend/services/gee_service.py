import numpy as np

def fetch_sar_imagery(bbox: list[float], start_date: str, end_date: str) -> np.ndarray:
    print(f"Fetching SAR imagery for bbox {bbox} from {start_date} to {end_date}")
    return np.random.rand(2, 256, 256)
