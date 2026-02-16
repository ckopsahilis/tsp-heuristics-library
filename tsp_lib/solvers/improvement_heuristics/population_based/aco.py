from ...base import BaseTSPSolver
import random
import numpy as np

class AntColonyOptimization(BaseTSPSolver):
    def __init__(self, dist_matrix, num_ants=20, max_iter=50, alpha=1.0, beta=2.0, evaporation_rate=0.5, Q=100):
        super().__init__(dist_matrix)
        self.num_ants = num_ants
        self.max_iter = max_iter
        self.alpha = alpha # Pheromone importance
        self.beta = beta   # Heuristic importance (1/dist)
        self.rho = evaporation_rate
        self.Q = Q
        
        # Heuristic information matrix (1 / distance)
        # Add small epsilon to avoid division by zero
        with np.errstate(divide='ignore'):
            self.heuristic = 1.0 / (self.dist_matrix + 1e-10)
        np.fill_diagonal(self.heuristic, 0)

    def solve(self):
        # Initialize pheromones
        # Start with small constant amount
        pheromone = np.ones((self.num_cities, self.num_cities)) * 0.1
        
        best_route = None
        best_cost = float('inf')
        
        for _ in range(self.max_iter):
            all_routes = []
            all_costs = []
            
            # Construct solutions
            for k in range(self.num_ants):
                route = [random.randint(0, self.num_cities - 1)]
                visited = set(route)
                
                current = route[0]
                while len(route) < self.num_cities:
                    # Calculate probabilities for moving to unvisited nodes
                    probs = []
                    candidates = []
                    
                    # To speed up, we can mask
                    # But simpler loop for clarity first
                    
                    denom = 0.0
                    
                    # Vectorized probability calculation for current node
                    # P_ij = (tau_ij^alpha) * (eta_ij^beta) / sum(...)
                    
                    # Get pheromone and heuristic row for current node
                    tau = pheromone[current]
                    eta = self.heuristic[current]
                    
                    # Calculate numerator
                    numerators = (tau ** self.alpha) * (eta ** self.beta)
                    
                    # Zero out visited
                    mask = np.ones(self.num_cities, dtype=bool)
                    mask[list(visited)] = False
                    
                    valid_numerators = numerators[mask]
                    valid_indices = np.where(mask)[0]
                    
                    if len(valid_indices) == 0: break # Should not happen if loop logic correct
                    
                    sum_prob = np.sum(valid_numerators)
                    if sum_prob == 0:
                        # Fallback to uniform if numerators are zero (unlikely but possible)
                        prob_dist = np.ones(len(valid_indices)) / len(valid_indices)
                    else:
                        prob_dist = valid_numerators / sum_prob
                        # Ensure sum is exactly 1.0 to avoid numpy errors
                        prob_dist = prob_dist / np.sum(prob_dist)
                    
                    # Choose next node
                    next_node = np.random.choice(valid_indices, p=prob_dist)
                    
                    route.append(next_node)
                    visited.add(next_node)
                    current = next_node
                
                cost = self.calculate_cost(route)
                all_routes.append(route)
                all_costs.append(cost)
                
                if cost < best_cost:
                    best_cost = cost
                    best_route = list(route)
            
            # Update Pheromones
            # Evaporation
            pheromone = (1 - self.rho) * pheromone
            
            # Deposit
            for i in range(self.num_ants):
                route = all_routes[i]
                cost = all_costs[i]
                deposit = self.Q / cost
                for j in range(self.num_cities - 1):
                    u, v = route[j], route[j+1]
                    pheromone[u, v] += deposit
                    pheromone[v, u] += deposit # Symmetric TSP
                # Last edge
                u, v = route[-1], route[0]
                pheromone[u, v] += deposit
                pheromone[v, u] += deposit
                
        return best_route
