import matplotlib.pyplot as plt
from grid import create_grid
from perception import load_mask
from regions import extract_rectangles

def main():
    grid = create_grid()
    mask = load_mask(grid.shape)
    rects = extract_rectangles(mask)
    start = (10, 10) #moglo bi se i mijenjati ali nek bude fiksno

    plt.figure(figsize=(6,6))
    plt.imshow(grid, cmap="Greens", origin="lower")

    # translucent color overlay for each label
    plt.imshow(mask, cmap="tab10", alpha=0.3, origin="lower")

    # draw rectangles with human-readable names
    for name, rect in rects.items():
        xs, ys = rect.exterior.xy
        plt.plot(xs, ys, linewidth=2, label=name.replace("_"," ").title())

    plt.scatter(*start, c="red", s=70, label="Start")
    plt.legend(loc="center right")
    plt.title("Field zones")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.tight_layout()
    plt.show()
    plt.savefig("../outputs/day1_named_overview.png")

if __name__ == "__main__":
    main()
