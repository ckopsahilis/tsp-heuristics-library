from ...base import BaseTSPSolver
import random
import math

class SimulatedAnnealing(BaseTSPSolver):
    def __init__(self, dist_matrix, initial_route=None, initial_temp=1000, cooling_rate=0.995, max_iter=10000):
        super().__init__(dist_matrix)
        self.initial_route = initial_route
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.max_iter = max_iter

    def solve(self):
        if self.initial_route is None:
            current_route = list(range(self.num_cities))
            random.shuffle(current_route)
        else:
            current_route = list(self.initial_route)
            
        current_cost = self.calculate_cost(current_route)
        best_route = list(current_route)
        best_cost = current_cost
        
        temp = self.initial_temp
        
        for _ in range(self.max_iter):
            # Swap two cities
            i, j = random.sample(range(self.num_cities), 2)
            new_route = list(current_route)
            new_route[i], new_route[j] = new_route[j], new_route[i]
            
            new_cost = self.calculate_cost(new_route)
            
            if new_cost < current_cost:
                current_route = new_route
                current_cost = new_cost
                if new_cost < best_cost:
                    best_route = list(new_route)
                    best_cost = new_cost
            else:
                prob = math.exp((current_cost - new_cost) / temp)
                if random.random() < prob:
                    current_route = new_route
                    current_cost = new_cost
            
            temp *= self.cooling_rate
            
        return best_route
