import numpy as np;
from expression_tree22 import Expression
import random
import logger

def generate_population(size, max_depth, functions, terminals, xSet, ySet):
    return [Expression(max_depth, functions, terminals, xSet , ySet) for _ in range(size)]

def select_parents(populations):
    return random.sample(populations, 2)

def genetic_programming(max_depth ,size, xSet, ySet, functions, terminals,xa,xb):
    num_generation = 0

    stall_generations = 0
    best_fitness_ever = float('inf')

    population = generate_population(size, max_depth,functions,terminals, xSet, ySet)
    while True:
        new_population = []
        children_population = []

        for _ in range(size):
            x, y = select_parents(population)
            if x.depth>50:
                x=Expression(max_depth, functions, terminals, xSet , ySet) 
            if y.depth>50:
                y=Expression(max_depth, functions, terminals, xSet , ySet)
            child1, child2 = x.crossover(y)

            if random.random() < 0.2:
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
            if random_number < 0.4:
                new_population.append(population.pop(0))
            elif random_number<0.6:
                new_population.append(Expression(max_depth, functions, terminals, xSet , ySet))
            else:
                new_population.append(children_population.pop(0))
        
        population = new_population
        num_generation += 1
        print(num_generation)
        fittest_individual = min(population)
    
        logger.log_data(num_generation,fittest_individual.fitness, terminals, size, max_depth)

        if fittest_individual.fitness < 1:
            break

        if fittest_individual.fitness < best_fitness_ever:
            best_fitness_ever = fittest_individual.fitness
            
            best_individual_ever = fittest_individual
            print(best_individual_ever.print_expression(best_individual_ever.root,xa,xb))
            print("Best fitness so far:", best_fitness_ever)
            stall_generations = 0
        else:
            stall_generations += 1

        if stall_generations >= 20:
            print("Termination criteria met: Best fitness has stalled.")
            return best_individual_ever, num_generation
        if  (num_generation >= 50 and best_fitness_ever>3) or num_generation>100:
            print("Termination criteria missed: Best fitness has stalled.")
            return best_individual_ever, num_generation

    return fittest_individual, num_generation