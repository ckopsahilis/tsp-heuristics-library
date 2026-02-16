from ....base import BaseTSPSolver
import random

class SwapLocalSearch(BaseTSPSolver):
    def solve(self):
        # Initial solution (random)
        route = list(range(self.num_cities))
        random.shuffle(route)
        
        improved = True
        while improved:
            improved = False
            best_delta = 0
            swap_pair = None
            
            # First improvement or Best improvement? Let's do Best Improvement for quality.
            for i in range(self.num_cities):
                for j in range(i + 1, self.num_cities):
                    # Swap i and j
                    # Calculate delta check is complex because they might be neighbors or not.
                    # Simplest way for code clarity: calculate full cost diff (expensive but robust)
                    # Optimization: standard delta evaluation
                    
                    old_cost = self.calculate_cost(route)
                    
                    route[i], route[j] = route[j], route[i]
                    new_cost = self.calculate_cost(route)
                    
                    if new_cost < old_cost:
                        # Found improvement
                        improved = True
                        # For First Improvement, break here. 
                        # For Best, continue. Let's do First Improvement for speed on N^2
                        break
                    else:
                        # Revert
                        route[i], route[j] = route[j], route[i]
                        
                if improved: break
                
        return route
