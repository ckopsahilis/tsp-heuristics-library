# TSP Library

A modular, extensible Python library for solving the Traveling Salesperson Problem (TSP). This library implements a wide range of construction and improvement heuristics, including trajectory-based and population-based metaheuristics.

## Features

- **Construction Heuristics**:
  - Nearest Neighbor
  - Greedy (Multi-Fragment)
  - Insertion Heuristics (Nearest, Cheapest, Farthest)
- **Improvement Heuristics**:
  - **Trajectory Based**: Simulated Annealing, Tabu Search, Local Search Operators (Swap, Relocate, 2-Opt, 3-Opt)
  - **Population Based**: Genetic Algorithm, Particle Swarm Optimization (PSO), Ant Colony Optimization (ACO)
- **Benchmark Tools**: Built-in script to benchmark all algorithms on standard TSPLIB instances.

## Installation

 Clone the repository:
   ```bash
   git clone https://github.com/ckopsahilis/tsp-heuristics-library.git
   cd tsp_library
   ```

## Usage

### Basic Usage

You can use the `main.py` script to run a demonstration on the `berlin52` instance:

```bash
python main.py
```

### Library Usage

```python
from tsp_lib.loader import TSPInstance
from tsp_lib.distance import compute_distance_matrix
from tsp_lib.solvers.improvement_heuristics import AntColonyOptimization

# 1. Load Data
instance = TSPInstance('instances/berlin52.tsp')
dist_matrix = compute_distance_matrix(instance.coords)

# 2. Initialize Solver
# Example: Ant Colony Optimization
solver = AntColonyOptimization(dist_matrix, num_ants=20, max_iter=50)

# 3. Solve
best_route = solver.solve()
cost = solver.calculate_cost(best_route)

print(f"Best Cost: {cost:.2f}")
print(f"Route: {best_route}")
```

## Benchmarks

We have benchmarked the algorithms on `berlin52`, `eil51`, and `st70`.

| Algorithm | Cost (berlin52) | Time (s) | Notes |
| :--- | :--- | :--- | :--- |
| **Ant Colony Optimization** | **8002.75** | 0.74 | High quality solutions. |
| **3-Opt Local Search** | 8150.95 | 8.51 | Strong local search. |
| **2-Opt Local Search** | 8187.49 | 0.05 | Fastest effective heuristic. |
| **Farthest Insertion** | 8308.60 | 0.01 | Best pure construction heuristic. |
| Nearest Neighbor | 8980.92 | ~0.00 | Baseline. |

See [benchmark_results.md](benchmark_results.md) for full details.

## Project Structure

```
tsp_lib/
├── loader.py           # Data loading
├── distance.py         # Distance calculations
└── solvers/
    ├── base.py         # Base solver class
    ├── construction_heuristics/
    │   ├── insertion_heuristic/
    │   └── ...
    └── improvement_heuristics/
        ├── trajectory_based/
        │   └── local_search_operators/
        └── population_based/
instances/              # TSPLIB instances
main.py                 # Demo script
benchmark.py            # Benchmark script
```

## Dependencies

- Python 3.x
- NumPy (`pip install numpy`)

## License

MIT License
