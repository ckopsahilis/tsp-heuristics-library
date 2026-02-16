from ....base import BaseTSPSolver
import random

class RelocateLocalSearch(BaseTSPSolver):
    def solve(self):
        # Initial solution (random)
        route = list(range(self.num_cities))
        random.shuffle(route)
        
        improved = True
        while improved:
            improved = False
            
            # First Improvement
            for i in range(self.num_cities):
                node = route[i]
                # Try inserting node i at position j
                for j in range(self.num_cities):
                    if i == j or j == i + 1: continue 
                    
                    old_cost = self.calculate_cost(route)
                    
                    # Perform relocate
                    # Remove i
                    temp_route = route[:i] + route[i+1:]
                    # Insert at j (if j > i, index shift handled by removal)
                    # Actually standard list insert logic:
                    # if inserting at j, effectively placing before current route[j]
                    
                    # Logic without temp list:
                    # Remove node
                    route.pop(i)
                    # If j > i, the index j has shifted down by 1
                    target_j = j - 1 if j > i else j
                    route.insert(target_j, node)
                    
                    new_cost = self.calculate_cost(route)
                    
                    if new_cost < old_cost:
                        improved = True
                        break
                    else:
                        # Revert
                        route.pop(target_j)
                        route.insert(i, node)
                        
                if improved: break
                
        return route
