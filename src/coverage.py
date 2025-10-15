import numpy as np
from shapely.geometry import LineString, Point
from shapely.affinity import rotate
from math import atan2, degrees

def generate_full_coverage(poly, spray_width):
    """
    Returns a list of (x,y) waypoints that fully sweep the rotated
    rectangle defined by 'poly' at spacing 'spray_width'.
    """
    # 1) Get the minimal rotated rectangle & its orientation
    rect = poly.minimum_rotated_rectangle
    coords = list(rect.exterior.coords)[:4]
    (x0, y0), (x1, y1) = coords[0], coords[1]
    angle = atan2(y1 - y0, x1 - x0)
    deg   = degrees(angle)
    center = rect.centroid.coords[0]

    # 2) Rotate polygon back to axis alignment
    poly_a = rotate(poly, -deg, origin=center, use_radians=False)
    minx, miny, maxx, maxy = poly_a.bounds

    # 3) Build vertical sweep lines across the aligned box
    xs = np.arange(minx, maxx + spray_width, spray_width)
    lines = [LineString([(x, miny), (x, maxy)]) for x in xs]

    # 4) Clip each line to the polygon and sample points
    path, rev = [], False
    for line in lines:
        seg = line.intersection(poly_a)
        if seg.is_empty:
            continue
        xcoords, ycoords = seg.xy
        N = int(max(abs(xcoords[-1] - xcoords[0]),
                    abs(ycoords[-1] - ycoords[0]))) + 1
        pts = list(zip(
            np.linspace(xcoords[0], xcoords[-1], N),
            np.linspace(ycoords[0], ycoords[-1], N)
        ))
        if rev:
            pts.reverse()
        path.extend(pts)
        rev = not rev

    # 5) Rotate waypoints back into the world frame
    world_path = [
        rotate(Point(x, y), deg, origin=center, use_radians=False).coords[0]
        for x, y in path
    ]
    return world_path


if __name__ == "__main__":
    # quick smoke test
    from shapely.geometry import box
    r = box(10, 10, 40, 25).minimum_rotated_rectangle
    sweep = generate_full_coverage(r, spray_width=5)
    print("Sample sweep points:", sweep[:5], "…", len(sweep), "points total")
