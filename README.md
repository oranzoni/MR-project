# Agricultural Drone Path Planning System

A comprehensive path planning and coverage system for agricultural drone operations targeting citrus disease management. This project combines RRT (Rapidly-exploring Random Tree) path planning, PDDL-based task planning, and full coverage path generation for autonomous drone navigation in agricultural fields with multiple disease zones.

## Overview

This system addresses the challenge of autonomous drone navigation in agricultural fields where different zones require different treatments. The drone must:
- Navigate around static obstacles and disease-infected zones
- Plan collision-free paths to multiple target regions
- Generate full coverage trajectories for pesticide spraying
- Schedule treatment tasks using automated planning (PDDL)
- Visualize field layouts, zones, and planned paths

### Key Features

- **RRT-based Path Planning**: Collision-free path generation from start position to multiple disease zones
- **Disease Zone Management**: Handles multiple citrus diseases (black spot, canker, melanose, greening) and healthy zones
- **Full Coverage Planning**: Generates sweeping patterns for complete pesticide application within zones
- **PDDL Task Planning**: Automated scheduling of drone operations (loading, flying, spraying)
- **Visualization Tools**: Rich plotting capabilities for field overview and path visualization

## Project Structure

```
MR-project-master/
│
├── main.py                    # Main entry point (minimal stub)
│
├── src/                       # Core source modules
│   ├── planiranje.py          # RRT path planning implementation
│   ├── perception.py          # Disease zone definitions and mask generation
│   ├── regions.py             # Rectangle extraction from zone masks
│   ├── grid.py                # Grid creation with static obstacles
│   ├── coverage.py            # Full coverage path generation
│   ├── visualize.py           # Visualization of field and zones
│   └── pddl_planner.py        # PDDL planner interface
│
├── pddl/                      # PDDL planning definitions
│   ├── domain.pddl            # Agrodrone domain (actions: load, fly, spray)
│   └── problem.pddl           # Problem instance (locations, pesticides, goals)
│
└── outputs/                   # Generated visualizations
    ├── day1_overview.png      # Field visualization with zones
    └── day1_named_overview.png # Named zone visualization
```

## Installation

### Prerequisites

- Python 3.7+
- pip package manager

### Required Dependencies

```bash
pip install numpy matplotlib shapely
```

For PDDL planning functionality:
```bash
pip install pyperplan
```

### Optional: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt  # If requirements.txt is created
```

## Usage

### 1. Visualize Field and Disease Zones

Generate a visual overview of the agricultural field with disease zones and obstacles:

```bash
cd src
python visualize.py
```

**Output**: Displays and saves field visualization with labeled zones to `outputs/day1_named_overview.png`

### 2. Run RRT Path Planning

Plan collision-free paths from start position to all disease zones:

```bash
cd src
python planiranje.py
```

**Features**:
- Plans paths to multiple zones (black_spot, canker, melanose, greening, healthy)
- Avoids static obstacles and disease zones (treated as obstacles during navigation)
- Uses goal-biased RRT with configurable parameters
- Visualizes all planned paths with color-coded routes

**Configuration** (in `planiranje.py`):
```python
MAX_ITER = 5000        # Maximum RRT iterations
STEP_SIZE = 10.0       # RRT step size
GOAL_BIAS = 0.9        # Goal-directed sampling probability (10% random)
GOAL_RADIUS = 5.0      # Goal reached threshold
```

### 3. Generate Coverage Paths

Create full coverage trajectories for pesticide spraying:

```bash
cd src
python coverage.py
```

**Output**: Generates sweeping waypoint patterns for complete zone coverage

### 4. PDDL Task Planning

Run the PDDL planner to generate task sequences:

```bash
cd src
python pddl_planner.py
```

**Requirements**: Requires `pyperplan` to be installed

**Planning Domain** (from `pddl/domain.pddl`):
- **Actions**: load, fly, spray
- **Objects**: locations (base, disease zones), pesticides (disease-specific)
- **Goal**: Spray all zones with appropriate pesticides and return to base

### 5. Extract Region Rectangles

Process disease zone masks to extract bounding rectangles:

```bash
cd src
python regions.py
```

## Configuration

### Disease Zones

Disease zones are defined in `src/perception.py`:

```python
zones = [
    (15, 145, 45, 175, "black_spot"),   # (x1, y1, x2, y2, label)
    (65, 115, 95, 145, "canker"),
    (105, 45, 135, 75, "melanose"),
    (145, 155, 175, 185, "greening"),
    (100, 20, 180, 40, "healthy")
]
```

**Label Map**:
```python
LABEL_MAP = {
    "background": 0,
    "healthy": 1,
    "black_spot": 2,
    "canker": 3,
    "melanose": 4,
    "greening": 5
}
```

### Static Obstacles

Defined in `src/grid.py` and `src/planiranje.py`:

```python
STATIC_OBSTACLES = [
    (180, 0, 200, 20),      # (x1, y1, x2, y2)
    (0, 180, 20, 200),
    (180, 180, 200, 200),
    (80, 80, 120, 120)
]
```

### Field Dimensions

Default: 200×200 units (configurable in `grid.py`)

```python
grid = create_grid(width=200, height=200)
```

### Start Position

Default start position: `(1.0, 1.0)` (configured in `planiranje.py`)

## Module Descriptions

### `planiranje.py` - Path Planning
**Main functionality**: RRT-based path planning

**Key Functions**:
- `rrt(start, goal, obstacles, bounds)`: Core RRT algorithm
- `collision_free(p1, p2, obstacles)`: Collision detection
- `compute_entry_points(zones, start)`: Calculate zone entry points (bottom-left corners)
- `build_obstacle_polygons(grid, obstacle_zones)`: Create obstacle representations

**Entry Point**: `main()` - Plans paths to all zones and visualizes results

### `perception.py` - Zone Management
**Purpose**: Define and generate disease zone masks

**Key Components**:
- `LABEL_MAP`: Disease label to integer mapping
- `zones`: List of zone definitions with coordinates
- `load_mask(shape)`: Generate 2D mask array with zone labels

### `regions.py` - Region Extraction
**Purpose**: Extract geometric regions from masks

**Key Functions**:
- `extract_rectangles(mask)`: Convert mask zones to minimal rotated rectangles using convex hull

**Dependencies**: Uses Shapely for geometric operations

### `grid.py` - Grid Generation
**Purpose**: Create environment grid with obstacles

**Key Functions**:
- `create_grid(width, height, obstacle_list)`: Generate 2D grid (0=free, 1=obstacle)

### `coverage.py` - Coverage Planning
**Purpose**: Generate full coverage paths for spraying

**Key Functions**:
- `generate_full_coverage(poly, spray_width)`: Create sweeping waypoint pattern
  - Aligns polygon to axis
  - Generates vertical sweep lines
  - Creates back-and-forth coverage pattern
  - Returns waypoints in world coordinates

**Parameters**:
- `poly`: Shapely polygon to cover
- `spray_width`: Spacing between sweep lines

### `visualize.py` - Visualization
**Purpose**: Generate field visualizations

**Output**:
- Displays grid with color-coded zones
- Draws extracted rectangles with labels
- Marks start position
- Saves to `outputs/day1_named_overview.png`

### `pddl_planner.py` - PDDL Interface
**Purpose**: Interface to PDDL planner

**Functionality**:
- Calls `pyperplan` with domain and problem files
- Captures and displays plan output

## PDDL Planning Details

### Domain (`pddl/domain.pddl`)

**Types**:
- `location`: Field positions (base, disease zones)
- `pesticide`: Treatment substances (disease-specific pesticides, water)

**Predicates**:
- `(at ?l - location)`: Drone location
- `(loaded ?p - pesticide)`: Pesticide loaded
- `(sprayed ?l - location ?p - pesticide)`: Zone treatment status

**Actions**:
1. **load**: Load pesticide at base
2. **fly**: Move between locations
3. **spray**: Apply pesticide at location

### Problem (`pddl/problem.pddl`)

**Objects**:
- Locations: base, black_spot, canker, melanose, greening, healthy
- Pesticides: black_spot_p, canker_p, melanose_p, greening_p, water

**Initial State**: Drone at base

**Goal**:
- Spray all disease zones with appropriate pesticides
- Spray healthy zone with water
- Return to base

## Inputs and Outputs

### Inputs

1. **Field Configuration**:
   - Grid dimensions: 200×200 (default)
   - Static obstacle locations
   - Disease zone definitions with coordinates

2. **Planning Parameters**:
   - RRT parameters (iterations, step size, goal bias)
   - Start position coordinates
   - Coverage spray width

### Outputs

1. **Visualizations** (`outputs/`):
   - Field overview with zones and obstacles
   - Path visualizations with planned routes

2. **Console Output**:
   - Path planning progress and results
   - Extracted region information
   - PDDL plan sequences

3. **Data Structures**:
   - Grid arrays (NumPy)
   - Zone masks (NumPy)
   - Path coordinates (lists of tuples)
   - Geometric polygons (Shapely)

## Algorithm Details

### RRT Path Planning

**Algorithm**: Goal-biased Rapidly-exploring Random Tree

**Process**:
1. Initialize tree with start position
2. For each iteration:
   - Sample point (90% toward goal, 10% random)
   - Find nearest tree node
   - Extend toward sample by step size
   - Check collision-free
   - Add to tree if valid
3. Check if goal reached (within GOAL_RADIUS)
4. Extract and return path

**Features**:
- Probabilistically complete
- Handles arbitrary obstacles
- Goal-biased for faster convergence

### Coverage Path Planning

**Algorithm**: Rotated sweep pattern

**Process**:
1. Compute minimal rotated rectangle for zone
2. Rotate zone to axis-aligned orientation
3. Generate vertical sweep lines at spray_width spacing
4. Clip lines to zone boundary
5. Sample waypoints along clipped segments
6. Alternate sweep direction (back-and-forth)
7. Rotate waypoints back to world frame

**Output**: Dense waypoint sequence for complete coverage

## Dependencies

### Core Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| numpy | Latest | Numerical operations, grid/mask arrays |
| matplotlib | Latest | Visualization and plotting |
| shapely | Latest | Geometric operations (polygons, collision detection) |
| pyperplan | Latest | PDDL planning (optional) |

### Standard Library

- `random`: RRT sampling
- `subprocess`: PDDL planner invocation
- `math`: Geometric calculations

## Notes and Limitations

### Known Limitations

1. **No requirements.txt**: Dependencies must be manually installed
2. **Hardcoded parameters**: Many configuration values embedded in source code
3. **2D planning only**: No altitude/3D considerations
4. **Static environment**: No dynamic obstacles or real-time replanning
5. **Simplified dynamics**: Point-mass drone model, no kinematic constraints

### Assumptions

- Drone can hover and make sharp turns (point-mass model)
- Disease zones are rectangular and axis-aligned (or rotated rectangles)
- Static obstacles are rectangular
- Sensor detection is perfect (no uncertainty)
- Pesticide application is instantaneous

### Future Enhancements

- Add requirements.txt with version pinning
- Configuration file (YAML/JSON) for parameters
- 3D path planning with altitude constraints
- Integration with real drone APIs (MAVLink, ROS)
- Dynamic obstacle avoidance
- Uncertainty handling and sensor fusion
- Path optimization (reduce waypoints, minimize turns)
- Multi-drone coordination
- Real-time replanning capabilities


## Authors

Project created for Mobile Robotics coursework focusing on autonomous agricultural drone systems.

**Contributors**: Haris Bešić, Amina Pojskić

## Acknowledgments

- RRT algorithm based on Steven LaValle's original work
- PDDL planning using pyperplan framework
- Shapely library for robust geometric operations
