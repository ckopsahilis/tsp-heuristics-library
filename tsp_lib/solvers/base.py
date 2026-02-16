from abc import ABC, abstractmethod
import numpy as np

class BaseTSPSolver(ABC):
    def __init__(self, dist_matrix):
        self.dist_matrix = dist_matrix
        self.num_cities = dist_matrix.shape[0]

    def calculate_cost(self, route):
        cost = 0
        for i in range(len(route) - 1):
            cost += self.dist_matrix[route[i], route[i+1]]
        cost += self.dist_matrix[route[-1], route[0]]
        return cost

    @abstractmethod
    def solve(self):
        pass
