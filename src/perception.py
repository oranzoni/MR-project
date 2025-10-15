### mask.py (disease zones)
import numpy as np

# sve bolesti u datasetu
LABEL_MAP = {"background": 0, "healthy": 1, "black_spot": 2,
               "canker": 3, "melanose": 4,
               "greening": 5}
# inverting a dictionary
INT_TO_NAME = {v: k for k, v in LABEL_MAP.items()}

# updates: moved zones to module level so they can be reused elsewhere
zones = [
    (15, 145,  45, 175, "black_spot"),  # updates: shifted left/down
    (65, 115,  95, 145, "canker"    ),  # updates: narrowed to open corridor
    (105, 45,  135,  75, "melanose"  ),  # updates: moved down slightly
    (145,155,  175,185, "greening"  ),  # updates: moved left/up slightly
    (100,   20, 180,  40, "healthy")  # updates: reduced width to avoid blocking
]

def load_mask(shape):
    """
    Returns a 2D mask labeling each zone according to LABEL_MAP.
    """
    mask = np.zeros(shape, dtype=int)
    for x1, y1, x2, y2, name in zones:  # updates: iterate over new module-level zones
        mask[y1:y2, x1:x2] = LABEL_MAP[name]
    return mask

if __name__ == "__main__":
    from grid import create_grid
    grid = create_grid()
    mask = load_mask(grid.shape)
    print("Mask labels:", np.unique(mask))  # → [0 1 2 3 4 5]
