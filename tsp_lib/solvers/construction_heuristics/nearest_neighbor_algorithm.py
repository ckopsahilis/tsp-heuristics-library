from ..base import BaseTSPSolver
import numpy as np

class NearestNeighbor(BaseTSPSolver):
    def solve(self):
        visited = [False] * self.num_cities
        route = [0]
        visited[0] = True
        
        current_node = 0
        for _ in range(self.num_cities - 1):
            distances = self.dist_matrix[current_node]
            # Set visited nodes distance to infinity to ignore them
            masked_distances = np.where(visited, np.inf, distances)
            next_node = np.argmin(masked_distances)
            
            route.append(int(next_node))
            visited[next_node] = True
            current_node = next_node
            
        return route
