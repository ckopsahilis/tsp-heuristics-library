import os
import time
import glob
from tsp_lib.loader import TSPInstance
from tsp_lib.distance import compute_distance_matrix

# Import all solvers
from tsp_lib.solvers import NearestNeighbor, SimulatedAnnealing, GeneticAlgorithm
from tsp_lib.solvers.construction_heuristics import GreedyAlgorithm
from tsp_lib.solvers.construction_heuristics.insertion_heuristic import NearestInsertion, CheapestInsertion, FarthestInsertion
from tsp_lib.solvers.improvement_heuristics import TabuSearch, ParticleSwarmOptimization, AntColonyOptimization
from tsp_lib.solvers.improvement_heuristics import SwapLocalSearch, RelocateLocalSearch, TwoOptLocalSearch, ThreeOptLocalSearch

def main():
    instance_files = glob.glob('instances/*.tsp')
    results = {} # instance -> {solver -> (cost, time)}

    for filepath in instance_files:
        filename = os.path.basename(filepath)
        print(f"Processing {filename}...")
        
        loader = TSPInstance(filepath)
        coords = loader.coords
        dist_matrix = compute_distance_matrix(coords)
        
        results[filename] = {}

        solvers = [
            ("Nearest Neighbor", lambda: NearestNeighbor(dist_matrix)),
            ("Greedy (Multi-Fragment)", lambda: GreedyAlgorithm(dist_matrix)),
            ("Nearest Insertion", lambda: NearestInsertion(dist_matrix)),
            ("Cheapest Insertion", lambda: CheapestInsertion(dist_matrix)),
            ("Farthest Insertion", lambda: FarthestInsertion(dist_matrix)),
            
            ("Simulated Annealing", lambda: SimulatedAnnealing(dist_matrix, max_iter=10000)), # Lower iters for benchmark speed
            ("Tabu Search", lambda: TabuSearch(dist_matrix, max_iter=200, tabu_tenure=10, neighbors_sample=20)),
            
            ("Genetic Algorithm", lambda: GeneticAlgorithm(dist_matrix, generations=100, pop_size=50)),
            ("Particle Swarm Optimization", lambda: ParticleSwarmOptimization(dist_matrix, num_particles=20, max_iter=50)),
            ("Ant Colony Optimization", lambda: AntColonyOptimization(dist_matrix, num_ants=10, max_iter=20)),
            
            ("Swap Local Search", lambda: SwapLocalSearch(dist_matrix)),
            ("Relocate Local Search", lambda: RelocateLocalSearch(dist_matrix)),
            ("2-Opt Local Search", lambda: TwoOptLocalSearch(dist_matrix)),
            ("3-Opt Local Search", lambda: ThreeOptLocalSearch(dist_matrix))
        ]
        
        for name, factory in solvers:
            print(f"  Running {name}...")
            start_time = time.time()
            try:
                solver = factory()
                route = solver.solve()
                cost = solver.calculate_cost(route)
                end_time = time.time()
                results[filename][name] = (cost, end_time - start_time)
            except Exception as e:
                print(f"    Failed: {e}")
                results[filename][name] = (float('inf'), 0)

    # Generate Markdown
    md_content = "# TSP Benchmark Findings\n\n"
    md_content += f"Generated on {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    for filename, instance_results in results.items():
        md_content += f"## Instance: {filename}\n\n"
        md_content += "| Algorithm | Cost | Time (s) |\n"
        md_content += "| :--- | :--- | :--- |\n"
        
        # Sort by cost
        sorted_results = sorted(instance_results.items(), key=lambda item: item[1][0])
        
        for name, (cost, duration) in sorted_results:
            md_content += f"| {name} | {cost:.2f} | {duration:.4f} |\n"
        md_content += "\n"

    with open('benchmark_results.md', 'w') as f:
        f.write(md_content)
    
    print("\nBenchmark complete. Results saved to benchmark_results.md")

if __name__ == "__main__":
    main()
