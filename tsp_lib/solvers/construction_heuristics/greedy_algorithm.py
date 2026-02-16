from ..base import BaseTSPSolver
import numpy as np

class GreedyAlgorithm(BaseTSPSolver):
    def solve(self):
        # Global Greedy (Multi-Fragment) Heuristic
        edges = []
        for i in range(self.num_cities):
            for j in range(i + 1, self.num_cities):
                edges.append((i, j, self.dist_matrix[i, j]))
        
        # Sort edges by weight
        edges.sort(key=lambda x: x[2])
        
        degrees = {i: 0 for i in range(self.num_cities)}
        adjacency = {i: [] for i in range(self.num_cities)}
        
        # Helper to check if u and v are in the same component
        parent = list(range(self.num_cities))
        def find(i):
            if parent[i] == i:
                return i
            return find(parent[i])
        
        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                parent[root_i] = root_j
                return True
            return False

        tour_edges = []
        edges_count = 0
        
        for u, v, w in edges:
            if degrees[u] < 2 and degrees[v] < 2:
                root_u = find(u)
                root_v = find(v)
                
                # Add edge if they are in different components OR it's the last edge closing the cycle
                if root_u != root_v or edges_count == self.num_cities - 1:
                    union(u, v)
                    adjacency[u].append(v)
                    adjacency[v].append(u)
                    degrees[u] += 1
                    degrees[v] += 1
                    tour_edges.append((u, v))
                    edges_count += 1
            
            if edges_count == self.num_cities:
                break
        
        # Reconstruct path
        route = [0]
        current = 0
        prev = -1
        visited_count = 1
        
        while visited_count < self.num_cities:
            neighbors = adjacency[current]
            found_next = False
            for n in neighbors:
                if n != prev:
                    route.append(n)
                    prev = current
                    current = n
                    visited_count += 1
                    found_next = True
                    break
            if not found_next:
                break
                
        return route
