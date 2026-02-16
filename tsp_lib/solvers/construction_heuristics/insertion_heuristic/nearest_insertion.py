from ...base import BaseTSPSolver
import numpy as np

class NearestInsertion(BaseTSPSolver):
    def solve(self):
        # 1. Start with a partial tour (node 0)
        route = [0]
        unvisited = set(range(1, self.num_cities))
        
        # 2. Find node j in unvisited closest to any node i in route
        while unvisited:
            min_dist = float('inf')
            next_node = -1
            
            # Find closest unvisited node to the tour
            for u in unvisited:
                for v in route:
                    if self.dist_matrix[u, v] < min_dist:
                        min_dist = self.dist_matrix[u, v]
                        next_node = u
            
            if next_node == -1: break # Should not happen unless unvisited is empty
            
            # 3. Insert next_node into route where it increases cost least
            best_pos = -1
            min_increase = float('inf')
            
            for i in range(len(route)):
                j = (i + 1) % len(route)
                u_node, v_node = route[i], route[j]
                # If only 1 node in route (start), dist(u, v) is 0. 
                # Cost increase: dist(u, new) + dist(new, u) - 0 = 2 * dist(u, new)
                
                increase = self.dist_matrix[u_node, next_node] + self.dist_matrix[next_node, v_node] - self.dist_matrix[u_node, v_node]
                if increase < min_increase:
                    min_increase = increase
                    best_pos = j
            
            # Insert at best_pos
            # if j=0 (end of list wrap around), insert at end? 
            # insert(index, object) inserts BEFORE index. 
            # if list is [A], i=0, j=0. best_pos=0. insert(0, B) -> [B, A]. Loop A-B-A. Correct. 
            # if list is [A, B]. i=0,j=1. insert(1, C) -> [A, C, B]. A-C-B-A. Correct.
            # if list is [A, B]. i=1,j=0. insert(0, C) -> [C, A, B]. C-A-B-C. Correct (order changed but loop same)
            # Actually if i=last, j=0. We want to insert AFTER last. 
            # If best_pos is 0 (wrapping), that means between last and first. 
            # Ideally simply append if i is last. 
            
            if best_pos == 0:
                route.append(next_node)
            else:
                route.insert(best_pos, next_node)
                
            unvisited.remove(next_node)
            
        return route
