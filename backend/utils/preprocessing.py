import numpy as np

def normalize_sar_image(image: np.ndarray) -> np.ndarray:
    min_val = np.min(image)
    max_val = np.max(image)
    if max_val - min_val == 0:
        return image
    return (image - min_val) / (max_val - min_val)

def tile_image(image: np.ndarray, tile_size: int = 256) -> list[np.ndarray]:
    _, h, w = image.shape
    tiles = []
    for y in range(0, h, tile_size):
        for x in range(0, w, tile_size):
            tile = image[:, y:y+tile_size, x:x+tile_size]
            tiles.append(tile)
    return tiles
