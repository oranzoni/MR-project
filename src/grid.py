import numpy as np

def create_grid(width=200, height=200, obstacle_list=None):
    """
    Returns a 2D array:
      0 = free
      1 = static obstacle
    Obstacles placed away from disease zones.
    """
    grid = np.zeros((height, width), dtype=int)

    # Static obstacles moved/enlarged to avoid any disease rectangles
    if obstacle_list is None:
        obstacle_list = [
            (180, 0, 200, 20),
            (0, 180, 20, 200),
            (180, 180, 200, 200),
            (80, 80, 120, 120),
        ]

    for x1, y1, x2, y2 in obstacle_list:
        grid[y1:y2, x1:x2] = 1

    return grid

if __name__ == "__main__":
    g = create_grid()
    print("Grid shape:", g.shape, "Unique values:", np.unique(g))
