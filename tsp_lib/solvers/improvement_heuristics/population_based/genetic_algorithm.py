from ...base import BaseTSPSolver
import random

class GeneticAlgorithm(BaseTSPSolver):
    def __init__(self, dist_matrix, pop_size=100, elite_size=20, mutation_rate=0.01, generations=500):
        super().__init__(dist_matrix)
        self.pop_size = pop_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.generations = generations

    def solve(self):
        population = self._initial_population()
        
        for _ in range(self.generations):
            population = self._next_generation(population)
            
        best_route = min(population, key=self.calculate_cost)
        return best_route

    def _initial_population(self):
        population = []
        for _ in range(self.pop_size):
            route = list(range(self.num_cities))
            random.shuffle(route)
            population.append(route)
        return population

    def _next_generation(self, current_gen):
        ranked_pop = sorted(current_gen, key=self.calculate_cost)
        selection_results = self._selection(ranked_pop)
        mating_pool = [ranked_pop[i] for i in selection_results]
        children = self._breed_population(mating_pool)
        next_gen = self._mutate_population(children)
        return next_gen

    def _selection(self, ranked_pop):
        selection_results = []
        # Elitism
        for i in range(self.elite_size):
            selection_results.append(i)
        
        # Roulette Wheel Selection
        fitness_inv = [1 / self.calculate_cost(r) for r in ranked_pop]
        total_fitness = sum(fitness_inv)
        probs = [f / total_fitness for f in fitness_inv]
        
        # Select remaining
        for _ in range(len(ranked_pop) - self.elite_size):
            pick = random.random()
            current = 0
            for i, prob in enumerate(probs):
                current += prob
                if current > pick:
                    selection_results.append(i)
                    break
        return selection_results

    def _breed_population(self, mating_pool):
        children = []
        # Keep elite
        for i in range(self.elite_size):
            children.append(mating_pool[i])
            
        pool = random.sample(mating_pool, len(mating_pool))
        
        for i in range(self.elite_size, len(mating_pool)):
            child = self._ordered_crossover(pool[i], pool[len(mating_pool)-i-1])
            children.append(child)
        return children

    def _ordered_crossover(self, parent1, parent2):
        start_pos = random.randint(0, self.num_cities - 1)
        end_pos = random.randint(0, self.num_cities - 1)
        
        start_p, end_p = min(start_pos, end_pos), max(start_pos, end_pos)
        
        child = [None] * self.num_cities
        for i in range(start_p, end_p + 1):
            child[i] = parent1[i]
            
        current_p2_idx = 0
        for i in range(self.num_cities):
            if child[i] is None:
                while parent2[current_p2_idx] in child:
                    current_p2_idx += 1
                child[i] = parent2[current_p2_idx]
        return child

    def _mutate_population(self, population):
        mutated_pop = []
        for idx in range(len(population)):
            mutated_pop.append(self._mutate(population[idx]))
        return mutated_pop

    def _mutate(self, individual):
        for swapped in range(len(individual)):
            if random.random() < self.mutation_rate:
                swap_with = int(random.random() * len(individual))
                individual[swapped], individual[swap_with] = individual[swap_with], individual[swapped]
        return individual
