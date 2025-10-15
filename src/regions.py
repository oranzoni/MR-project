import numpy as np
from shapely.geometry import Point
from shapely.ops import unary_union
from perception import INT_TO_NAME
from perception import load_mask

#izvuci ce kvadrate za svaku regiju
def extract_rectangles(mask):

    rectangles = {}
    for label in np.unique(mask):

        name = INT_TO_NAME[label]
        ys, xs = np.where(mask == label)
        points = [Point(x, y) for x, y in zip(xs, ys)]
        poly = unary_union(points).convex_hull
        rectangles[name] = poly.minimum_rotated_rectangle
    return rectangles

if __name__ == "__main__":

    mask = load_mask((200, 200))
    rects = extract_rectangles(mask)
    print("Extracted for:", rects.keys())
    # → dict_keys(['black_spot', 'canker', 'melanose', 'greening', 'healthy'])
