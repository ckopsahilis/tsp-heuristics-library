from ...base import BaseTSPSolver
import random
from collections import deque

class TabuSearch(BaseTSPSolver):
    def __init__(self, dist_matrix, max_iter=1000, tabu_tenure=20, neighbors_sample=50):
        super().__init__(dist_matrix)
        self.max_iter = max_iter
        self.tabu_tenure = tabu_tenure
        self.neighbors_sample = neighbors_sample

    def solve(self):
        # Initial solution (random)
        current_route = list(range(self.num_cities))
        random.shuffle(current_route)
        
        best_route = list(current_route)
        best_cost = self.calculate_cost(best_route)
        
        # Tabu list stores (i, j) swaps that are forbidden
        # Using a deque for FIFO tenure
        tabu_list = deque(maxlen=self.tabu_tenure)
        
        for _ in range(self.max_iter):
            best_neighbor = None
            best_neighbor_cost = float('inf')
            best_move = None
            
            # Generate neighborhood (Swap)
            # Full neighborhood is O(N^2), too slow to do every iter if N is large.
            # We sample a subset of neighbors for efficiency.
            
            for _ in range(self.neighbors_sample):
                i, j = random.sample(range(self.num_cities), 2)
                if i > j: i, j = j, i
                
                # Check if move is tabu
                is_tabu = (i, j) in tabu_list
                
                # Create neighbor
                neighbor = list(current_route)
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbor_cost = self.calculate_cost(neighbor)
                
                # Aspiration criteria: allow tabu move if it improves global best
                if is_tabu and neighbor_cost >= best_cost:
                    continue
                
                if neighbor_cost < best_neighbor_cost:
                    best_neighbor = neighbor
                    best_neighbor_cost = neighbor_cost
                    best_move = (i, j)
            
            if best_neighbor:
                current_route = best_neighbor
                if best_neighbor_cost < best_cost:
                    best_route = list(best_neighbor)
                    best_cost = best_neighbor_cost
                
                # Add move to tabu list
                tabu_list.append(best_move)
            
        return best_route
