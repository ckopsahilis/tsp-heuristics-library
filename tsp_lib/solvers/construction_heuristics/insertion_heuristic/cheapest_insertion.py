from ...base import BaseTSPSolver
import numpy as np

class CheapestInsertion(BaseTSPSolver):
    def solve(self):
        # 1. Start with partial tour (0, closest to 0) to form a loop
        # Finding closest to 0 to make a subtour 0-k-0
        first_node = 0
        dists_from_0 = self.dist_matrix[0]
        # Mask 0 itself
        dists_from_0[0] = np.inf
        second_node = np.argmin(dists_from_0)
        
        route = [first_node, int(second_node)]
        unvisited = set(range(self.num_cities))
        unvisited.remove(first_node)
        unvisited.remove(second_node)
        
        while unvisited:
            best_node = -1
            best_pos = -1
            min_increase = float('inf')
            
            # Find (k, i, j) that minimizes C_ik + C_kj - C_ij
            for k in unvisited:
                for i in range(len(route)):
                    j = (i + 1) % len(route)
                    u, v = route[i], route[j]
                    increase = self.dist_matrix[u, k] + self.dist_matrix[k, v] - self.dist_matrix[u, v]
                    
                    if increase < min_increase:
                        min_increase = increase
                        best_node = k
                        best_pos = j
            
            if best_pos == 0:
                route.append(best_node)
            else:
                route.insert(best_pos, best_node)
            
            unvisited.remove(best_node)
            
        return route
