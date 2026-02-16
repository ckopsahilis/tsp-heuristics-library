from ...base import BaseTSPSolver
import numpy as np

class FarthestInsertion(BaseTSPSolver):
    def solve(self):
        # 1. Start with node 0 (and its farthest node to make a pair? Or just node 0)
        # Using node 0 and finding the farthest from it to start a loop is common, 
        # but let's stick to the pattern: Start with partial tour [0]
        route = [0]
        unvisited = set(range(1, self.num_cities))
        
        while unvisited:
            # 2. Find node k in unvisited FARTHEST from any node in route (max-min distance)
            max_min_dist = -1
            next_node = -1
            
            for u in unvisited:
                # Distance from u to the set of nodes in route is the MIN distance to any node in route
                min_dist_to_route = float('inf')
                for v in route:
                    d = self.dist_matrix[u, v]
                    if d < min_dist_to_route:
                        min_dist_to_route = d
                
                if min_dist_to_route > max_min_dist:
                    max_min_dist = min_dist_to_route
                    next_node = u
            
            # 3. Insert next_node into route where it increases cost least
            best_pos = -1
            min_increase = float('inf')
            
            for i in range(len(route)):
                j = (i + 1) % len(route)
                u, v = route[i], route[j]
                increase = self.dist_matrix[u, next_node] + self.dist_matrix[next_node, v] - self.dist_matrix[u, v]
                
                if increase < min_increase:
                    min_increase = increase
                    best_pos = j
            
            # Since route is a list of nodes, inserting at index j means between i and j?
            # route = [a, b, c]. len=3. i=0, j=1. u=a, v=b. Insert at 1 -> [a, new, b, c]
            # correct.
            route.insert(best_pos, next_node)
            unvisited.remove(next_node)
            
        return route
