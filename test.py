import csv
import numpy as np
from expression_tree import Expression
from genetic import*
import matplotlib.pyplot as plt

xSet = []
ySet = []
with open('dataset1.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        x, y = map(float, row)
        xSet.append(x)
        ySet.append(y)

xSet = np.array(xSet)
ySet = np.array(ySet)

# Parameters
terminals = ['x', 1, 2, 3]
functions = ['+', '-', '*', '/']
max_depth = 3
population_size = 70

best_expression = genetic_programming(max_depth=max_depth, size=population_size, xSet=xSet, ySet=ySet, functions= functions, terminals= terminals)

print("Best Expression:", best_expression.print_expression(best_expression.root))
print("Best Fitness:", best_expression.fitness)


x_values = np.linspace(min(xSet), max(xSet), 400)
y_values = [best_expression.evaluate(best_expression.root, x) for x in x_values]

plt.scatter(xSet, ySet, c='blue', label='Dataset')

plt.plot(x_values, y_values, c='red', label='Best-fit function')

plt.legend()
plt.show()
