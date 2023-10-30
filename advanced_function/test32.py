import csv
import numpy as np
from genetic32 import*
import time

xSet = []
ySet = []
time1=time.perf_counter()
with open('dataset3.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        x, y = map(float, row)
        xSet.append(x)
        ySet.append(y)

xSet = np.array(xSet)
ySet = np.array(ySet)

# Parameters
terminals = ['x', 1, 2, 3,4,5]
functions = ['+', '-', '*', '/','exp','log','sin','cos']
max_depth = 5
population_size = 350

best_expression = genetic_programming(max_depth=max_depth, size=population_size, xSet=xSet[:500], ySet=ySet[:500], functions= functions, terminals= terminals)
best_eval=best_expression.exeval(xSet[500:],ySet[500:])
txtime=time.perf_counter()
print(txtime)
for i in range(500):
    new_best=genetic_programming(max_depth=max_depth, size=population_size, xSet=xSet[:500], ySet=ySet[:500], functions= functions, terminals= terminals)
    if new_best.exeval(xSet[500:],ySet[500:])<best_eval:
        best_expression=new_best
        best_eval=best_expression.exeval(xSet[500:],ySet[500:])
    print('which round')
    print(i)
    timeused=time.perf_counter()-txtime
    txtime=time.perf_counter()
    print('timeused:')
    print(timeused)
    
    print("Best Expression:", best_expression.print_expression(best_expression.root))
    print("Best Fitness:", best_expression.fitness)
    print("Best Eval:", best_eval)
    if timeused>43200:
        break
    
    
    
print("Best Expression:", best_expression.print_expression(best_expression.root))
print("Best Fitness:", best_expression.fitness)
print("Best Eval:", best_eval)

time2=time.perf_counter()
print(time2-time1)