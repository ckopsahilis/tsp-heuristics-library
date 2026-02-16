from ....base import BaseTSPSolver
import random

class TwoOptLocalSearch(BaseTSPSolver):
    def solve(self):
        # Initial solution (random)
        route = list(range(self.num_cities))
        random.shuffle(route)
        
        improved = True
        while improved:
            improved = False
            for i in range(self.num_cities - 1):
                for j in range(i + 1, self.num_cities):
                    if j - i == 1: continue
                    
                    if self._two_opt_gain(route, i, j) < 0:
                        route[i:j] = reversed(route[i:j]) # Reverse segment
                        improved = True
                        break
                if improved: break
        
        return route

    def _two_opt_gain(self, route, i, j):
        # Check if swapping edges (i-1, i) and (j-1, j) to (i-1, j-1) and (i, j) improves cost
        # i is start of segment, j is end (exclusive) in slice notation
        # nodes are: A=route[i-1], B=route[i], C=route[j-1], D=route[j % N]
        
        a = route[i-1]
        b = route[i]
        c = route[j-1]
        d = route[j % self.num_cities]
        
        old_dist = self.dist_matrix[a, b] + self.dist_matrix[c, d]
        new_dist = self.dist_matrix[a, c] + self.dist_matrix[b, d]
        
        return new_dist - old_dist
