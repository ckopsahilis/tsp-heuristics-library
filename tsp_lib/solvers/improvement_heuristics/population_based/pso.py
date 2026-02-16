from ...base import BaseTSPSolver
import random
import numpy as np

class ParticleSwarmOptimization(BaseTSPSolver):
    def __init__(self, dist_matrix, num_particles=30, max_iter=100, w=0.5, c1=1, c2=2):
        super().__init__(dist_matrix)
        self.num_particles = num_particles
        self.max_iter = max_iter
        self.w = w      # Inertia
        self.c1 = c1    # Cognitive (local best)
        self.c2 = c2    # Social (global best)

    def solve(self):
        # Using Random Keys encoding:
        # Particle position is a continuous vector of length N.
        # Permutation is obtained by sorting indices based on vector values.
        
        # Initialize particles
        # Position: [N, num_cities]
        # Velocity: [N, num_cities]
        positions = np.random.rand(self.num_particles, self.num_cities)
        velocities = np.random.rand(self.num_particles, self.num_cities) * 0.2 - 0.1 # Small random velocities
        
        personal_best_pos = np.copy(positions)
        personal_best_scores = np.full(self.num_particles, np.inf)
        
        global_best_pos = None
        global_best_score = float('inf')
        global_best_route = None
        
        for iteration in range(self.max_iter):
            for i in range(self.num_particles):
                # Decode position to route
                # argsort gives indices that would sort the array
                route = np.argsort(positions[i])
                cost = self.calculate_cost(route)
                
                # Update personal best
                if cost < personal_best_scores[i]:
                    personal_best_scores[i] = cost
                    personal_best_pos[i] = np.copy(positions[i])
                    
                    # Update global best
                    if cost < global_best_score:
                        global_best_score = cost
                        global_best_pos = np.copy(positions[i])
                        global_best_route = list(route)
            
            # Update velocities and positions
            # V(t+1) = w*V(t) + c1*rand*(pbest - x) + c2*rand*(gbest - x)
            
            r1 = np.random.rand(self.num_particles, self.num_cities)
            r2 = np.random.rand(self.num_particles, self.num_cities)
            
            velocities = (self.w * velocities + 
                          self.c1 * r1 * (personal_best_pos - positions) + 
                          self.c2 * r2 * (global_best_pos - positions))
            
            positions = positions + velocities
            
        return list(global_best_route) if global_best_route is not None else list(range(self.num_cities))
