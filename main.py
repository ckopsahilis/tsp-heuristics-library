from tsp_lib.loader import TSPInstance
from tsp_lib.distance import compute_distance_matrix
from tsp_lib.solvers import NearestNeighbor, SimulatedAnnealing, GeneticAlgorithm
from tsp_lib.solvers.construction_heuristics import GreedyAlgorithm
from tsp_lib.solvers.construction_heuristics.insertion_heuristic import NearestInsertion, CheapestInsertion, FarthestInsertion
from tsp_lib.solvers.improvement_heuristics import TabuSearch, ParticleSwarmOptimization, AntColonyOptimization
from tsp_lib.solvers.improvement_heuristics import SwapLocalSearch, RelocateLocalSearch, TwoOptLocalSearch, ThreeOptLocalSearch
import os
import time

def main():
    filepath = 'instances/berlin52.tsp'
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return

    print("Loading data...")
    loader = TSPInstance(filepath)
    coords = loader.coords
    print(f"Loaded {len(coords)} cities.")

    print("Computing distance matrix...")
    dist_matrix = compute_distance_matrix(coords)

    print("\n" + "="*40)
    print("      CONSTRUCTION HEURISTICS")
    print("="*40)

    # Nearest Neighbor
    print("\n--- Nearest Neighbor ---")
    start_time = time.time()
    nn = NearestNeighbor(dist_matrix)
    nn_route = nn.solve()
    nn_cost = nn.calculate_cost(nn_route)
    print(f"Cost: {nn_cost:.2f}")
    print(f"Time: {time.time() - start_time:.4f}s")

    # Greedy Algorithm (Multi-Fragment)
    print("\n--- Greedy (Multi-Fragment) ---")
    start_time = time.time()
    greedy = GreedyAlgorithm(dist_matrix)
    greedy_route = greedy.solve()
    greedy_cost = greedy.calculate_cost(greedy_route)
    print(f"Cost: {greedy_cost:.2f}")
    print(f"Time: {time.time() - start_time:.4f}s")

    # Nearest Insertion
    print("\n--- Nearest Insertion ---")
    start_time = time.time()
    ni = NearestInsertion(dist_matrix)
    ni_route = ni.solve()
    ni_cost = ni.calculate_cost(ni_route)
    print(f"Cost: {ni_cost:.2f}")
    print(f"Time: {time.time() - start_time:.4f}s")
    
    # Cheapest Insertion
    print("\n--- Cheapest Insertion ---")
    start_time = time.time()
    ci = CheapestInsertion(dist_matrix)
    ci_route = ci.solve()
    ci_cost = ci.calculate_cost(ci_route)
    print(f"Cost: {ci_cost:.2f}")
    print(f"Time: {time.time() - start_time:.4f}s")
    
    # Farthest Insertion
    print("\n--- Farthest Insertion ---")
    start_time = time.time()
    fi = FarthestInsertion(dist_matrix)
    fi_route = fi.solve()
    fi_cost = fi.calculate_cost(fi_route)
    print(f"Cost: {fi_cost:.2f}")
    print(f"Time: {time.time() - start_time:.4f}s")

    print("\n" + "="*40)
    print("      IMPROVEMENT HEURISTICS")
    print("="*40)

    print("\n[Trajectory Based]")
    # Simulated Annealing
    print("\n--- Simulated Annealing ---")
    start_time = time.time()
    # Using NN result as initial route for SA is common, but let's stick to standard behavior for fair comparison unless specified
    # Using nn_route here as in previous version
    sa = SimulatedAnnealing(dist_matrix, initial_route=nn_route, max_iter=100000)
    sa_route = sa.solve()
    sa_cost = sa.calculate_cost(sa_route)
    print(f"Cost: {sa_cost:.2f}")
    print(f"Time: {time.time() - start_time:.4f}s")

    # Tabu Search
    print("\n--- Tabu Search ---")
    start_time = time.time()
    tabu = TabuSearch(dist_matrix, max_iter=500, tabu_tenure=20, neighbors_sample=50)
    tabu_route = tabu.solve()
    tabu_cost = tabu.calculate_cost(tabu_route)
    print(f"Cost: {tabu_cost:.2f}")
    print(f"Time: {time.time() - start_time:.4f}s")
    
    print("\n[Local Search Operators (Trajectory Based)]")
    # Swap
    print("\n--- Swap Local Search ---")
    start_time = time.time()
    swap = SwapLocalSearch(dist_matrix)
    swap_route = swap.solve()
    swap_cost = swap.calculate_cost(swap_route)
    print(f"Cost: {swap_cost:.2f}")
    print(f"Time: {time.time() - start_time:.4f}s")
    
    # Relocate
    print("\n--- Relocate Local Search ---")
    start_time = time.time()
    relocate = RelocateLocalSearch(dist_matrix)
    relocate_route = relocate.solve()
    relocate_cost = relocate.calculate_cost(relocate_route)
    print(f"Cost: {relocate_cost:.2f}")
    print(f"Time: {time.time() - start_time:.4f}s")
    
    # 2-Opt
    print("\n--- 2-Opt Local Search ---")
    start_time = time.time()
    two_opt = TwoOptLocalSearch(dist_matrix)
    two_opt_route = two_opt.solve()
    two_opt_cost = two_opt.calculate_cost(two_opt_route)
    print(f"Cost: {two_opt_cost:.2f}")
    print(f"Time: {time.time() - start_time:.4f}s")
    
    # 3-Opt
    print("\n--- 3-Opt Local Search ---")
    start_time = time.time()
    three_opt = ThreeOptLocalSearch(dist_matrix)
    three_opt_route = three_opt.solve()
    three_opt_cost = three_opt.calculate_cost(three_opt_route)
    print(f"Cost: {three_opt_cost:.2f}")
    print(f"Time: {time.time() - start_time:.4f}s")

    print("\n[Population Based]")
    # Genetic Algorithm
    print("\n--- Genetic Algorithm ---")
    start_time = time.time()
    ga = GeneticAlgorithm(dist_matrix, generations=500, pop_size=100, elite_size=20)
    ga_route = ga.solve()
    ga_cost = ga.calculate_cost(ga_route)
    print(f"Cost: {ga_cost:.2f}")
    print(f"Time: {time.time() - start_time:.4f}s")

    # Particle Swarm Optimization
    print("\n--- Particle Swarm Optimization ---")
    start_time = time.time()
    pso = ParticleSwarmOptimization(dist_matrix, num_particles=30, max_iter=100)
    pso_route = pso.solve()
    pso_cost = pso.calculate_cost(pso_route)
    print(f"Cost: {pso_cost:.2f}")
    print(f"Time: {time.time() - start_time:.4f}s")
    
    # Ant Colony Optimization
    print("\n--- Ant Colony Optimization ---")
    start_time = time.time()
    aco = AntColonyOptimization(dist_matrix, num_ants=20, max_iter=50)
    aco_route = aco.solve()
    aco_cost = aco.calculate_cost(aco_route)
    print(f"Cost: {aco_cost:.2f}")
    print(f"Time: {time.time() - start_time:.4f}s")

if __name__ == "__main__":
    main()
