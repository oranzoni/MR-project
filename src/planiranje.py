import random
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString

from grid       import create_grid
from perception import load_mask, LABEL_MAP
from regions    import extract_rectangles

# static obstacles for plotting and collision
STATIC_OBSTACLES = [
    (180,  0,  200, 20),
    (0,  180,   20,200),
    (180,180,  200,200),
    (80,  80,  120,120),
]

# ——— RRT PARAMETERS ———
MAX_ITER    = 5000
STEP_SIZE   = 10.0
GOAL_BIAS   = 0.9     # 10% goal‐directed
GOAL_RADIUS = 5.0     # consider goal reached

# Euclidean distance
def euclid(a, b):
    return np.hypot(a[0] - b[0], a[1] - b[1])

# Build polygons for static obstacles and given zones
def build_obstacle_polygons(grid, obstacle_zones):
    """
    Returns list of polygons:
      • static obstacles
      • zones to treat as obstacles (diseases)
    """
    polys = [Polygon([(x1,y1),(x2,y1),(x2,y2),(x1,y2)])
             for x1,y1,x2,y2 in STATIC_OBSTACLES]
    polys += list(obstacle_zones.values())
    return polys

# Check segment p1->p2 is collision-free

def collision_free(p1, p2, obstacles):
    seg = LineString([p1, p2])
    return all(not (seg.crosses(o) or seg.within(o)) for o in obstacles)

# RRT routine
def rrt(start, goal, obstacles, bounds):
    nodes = {0: {'pt': start, 'parent': None}}
    for i in range(1, MAX_ITER):
        sample = goal if random.random() < GOAL_BIAS else (
            random.uniform(0, bounds[0]),
            random.uniform(0, bounds[1]))
        nearest = min(nodes, key=lambda n: euclid(nodes[n]['pt'], sample))
        p_near, d = nodes[nearest]['pt'], euclid(nodes[nearest]['pt'], sample)
        if d == 0: continue
        alpha = min(STEP_SIZE/d, 1.0)
        new_pt = (p_near[0] + alpha*(sample[0] - p_near[0]),
                  p_near[1] + alpha*(sample[1] - p_near[1]))
        if not collision_free(p_near, new_pt, obstacles): continue
        nodes[i] = {'pt': new_pt, 'parent': nearest}
        # goal check
        if euclid(new_pt, goal) < GOAL_RADIUS and collision_free(new_pt, goal, obstacles):
            nodes[i+1] = {'pt': goal, 'parent': i}
            path, cur = [], i+1
            while cur is not None:
                path.append(nodes[cur]['pt'])
                cur = nodes[cur]['parent']
            return list(reversed(path))
    raise RuntimeError(f"RRT failed to find path to {goal}")

# Choose bottom-left corner of each zone as entry
def compute_entry_points(zones, start):
    entries = {}
    for name, poly in zones.items():
        corners = list(poly.exterior.coords)[:-1]
        min_y   = min(y for x,y in corners)
        cands   = [(x,y) for x,y in corners if y == min_y]
        entries[name] = min(cands, key=lambda p: p[0])
    return entries

# Main script
def main():
    # 1) load grid and mask
    grid  = create_grid()
    mask  = load_mask(grid.shape)
    rects = extract_rectangles(mask)

    # 2) split into obstacles (diseases) and goal zones (include healthy)
    obstacle_zones = {n:p for n,p in rects.items() if n not in ("background","healthy")}
    goal_zones     = {n:p for n,p in rects.items() if n != "background"}

    # 3) set start point
    start = (1.0, 1.0)

    # 4) compute entry points for all goal zones
    entries = compute_entry_points(goal_zones, start)

    # 5) build obstacle list and bounds
    obstacles = build_obstacle_polygons(grid, obstacle_zones)
    bounds    = (grid.shape[1], grid.shape[0])

    # 6) plan paths to each zone
    paths = {}
    for name, goal in entries.items():
        print(f"Planning to {name} -> {goal}")
        paths[name] = rrt(start, goal, obstacles, bounds)

    # 7) plot everything
    plt.figure(figsize=(6,6))

    # static obstacles (grey fill)
    for i,(x1,y1,x2,y2) in enumerate(STATIC_OBSTACLES):
        xs = [x1, x2, x2, x1]
        ys = [y1, y1, y2, y2]
        plt.fill(xs, ys, facecolor='grey', edgecolor='black', alpha=0.5,
                 label='Obstacle' if i == 0 else '_nolegend_')

    # disease zones (dashed)
    for name, poly in obstacle_zones.items():
        xs, ys = poly.exterior.xy
        plt.plot(xs, ys, '--', lw=2, label='_nolegend_')

    # healthy zone (solid green)
    if 'healthy' in goal_zones:
        hpoly = goal_zones['healthy']
        xs, ys = hpoly.exterior.xy
        plt.plot(xs, ys, '-', lw=2, label='Healthy Zone')

    # start point
    plt.scatter(*start, c='red', s=60, label='Start')

    # plot each path
    for name, path in paths.items():
        xs, ys = zip(*path)
        lbl = 'Healthy Path' if name == 'healthy' else name.replace('_',' ').title()
        plt.plot(xs, ys, '-', lw=2, label=lbl)

    plt.legend(loc='center right', fontsize='small')
    plt.title('2D RRT Paths to Zones')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
