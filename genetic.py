import numpy as np;
from expression_tree import Expression
import random

def generate_population(size, max_depth, functions, terminals, xSet, ySet):
    return [Expression(max_depth, functions, terminals, xSet , ySet) for _ in range(size)]

def select_parents(populations):
    return random.sample(populations, 2)

def genetic_programming(max_depth ,size, xSet, ySet, functions, terminals):
    num_generation = 0

    stall_generations = 0
    best_fitness_ever = float('inf')

    population = generate_population(size, max_depth,functions,terminals, xSet, ySet)
    while True:
        new_population = []
        children_population = []

        for _ in range(size):
            x, y = select_parents(population)

            child1, child2 = x.crossover(y)

            if random.random() < 0.1:
                mutate_child1 = child1.mutate()
                mutate_child2 = child2.mutate()
                children_population.append(mutate_child1)
                children_population.append(mutate_child2)
            
            children_population.append(child1)
            children_population.append(child2)

        population.sort()
        children_population.sort()

        while len(new_population) < size:
            random_number = random.random()
            if random_number < 0.2:
                new_population.append(population.pop(0))
            else: 
                new_population.append(children_population.pop(0))
        
        population = new_population
        num_generation += 1
        print(num_generation)
        fittest_individual = min(population)

        if fittest_individual.fitness < 1:
            break

        if fittest_individual.fitness < best_fitness_ever:
            best_fitness_ever = fittest_individual.fitness
            best_individual_ever = fittest_individual
            print("Best fitness so far:", best_fitness_ever)
            stall_generations = 0
        else:
            stall_generations += 1
        if stall_generations >= 10:
            print("Termination criteria met: Best fitness has stalled.")
            return best_individual_ever

    return fittest_individual




