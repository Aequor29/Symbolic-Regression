import csv
import numpy as np
from genetic_d2 import*
import matplotlib.pyplot as plt
import time

xSet = []
ySet = []

x1a, x2a, x3a,x1b,x2b,x3b=0,0,0,1,1,1
time1=time.perf_counter()
with open('dataset2.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        x1,x2,x3, y = map(float,row)
        xSet.append(np.array([x1,x2,x3]))
        ySet.append(y)

lower_bound, upper_bound = np.percentile(ySet, [5, 95])
filtered_indices = np.where((ySet >= lower_bound) & (ySet <= upper_bound))
xSet = np.array(xSet)[filtered_indices]
ySet = np.array(ySet)[filtered_indices]

xa=[min([x[0] for x in xSet]),min([x[1] for x in xSet]),min([x[2] for x in xSet])]
xb=[max([x[0] for x in xSet])-min([x[0] for x in xSet]),max([x[1] for x in xSet])-min([x[1] for x in xSet]),max([x[2] for x in xSet])-min([x[2] for x in xSet])]
x1a,x2a,x3a=xa[0],xa[1],xa[2]
x1b,x2b,x3b=xb[0],xb[1],xb[2]
xSet = np.array([np.array([(x[0]-x1a)/x1b,(x[1]-x2a)/x2b,(x[2]-x3a)/x3b]) for x in xSet])
ySet = np.array(ySet)


# Parameters
terminals = ['c', 'x1','x2','x3']
functions = ['+', '-', '*', '/']

max_depth = 7
population_size = 350

best_expression = genetic_programming(max_depth=max_depth, size=population_size, xSet=xSet[:3000], ySet=ySet[:3000], functions= functions, terminals= terminals,xa=xa,xb=xb)
best_eval=best_expression.exeval(xSet,ySet)
txtime=time.perf_counter()
print(f'Time used: {txtime}')
print(f'Best Expression: {best_expression.print_expression(best_expression.root, xa, xb)}')
print(f'Best Fitness: {best_expression.fitness}')
print(f'Best Eval: {best_eval}')



for i in range(500):
    new_best = genetic_programming(max_depth=max_depth, size=population_size, xSet=xSet[:3000], ySet=ySet[:3000], functions= functions, terminals= terminals, xa=xa, xb=xb)
    new_best_eval = new_best.exeval(xSet, ySet)
    
    if new_best_eval < best_eval:
        best_expression = new_best
        best_eval = new_best_eval

    print(f'Round: {i+1}')
    timeused = time.perf_counter() - txtime
    txtime = time.perf_counter()

    print(f'Time used: {timeused}')
    print(f'Best Expression: {best_expression.print_expression(best_expression.root, xa, xb)}')
    print(f'Best Fitness: {best_expression.fitness}')
    print(f'Best Eval: {new_best_eval}')
    print(f'Best Eval_ever: {best_eval}')
    
    # Termination conditions
    if timeused > 10800 or best_eval < 3:
        break

    
    
    
print("Best Expression:", best_expression.print_expression(best_expression.root,xa,xb))
print("Best Fitness:", best_expression.fitness)
print("Best Eval:", best_eval)

time2=time.perf_counter()
print(time2-time1)


x_test = xSet[3000:]
y_true = ySet[3000:]

y_pred = [best_expression.evaluate(x) for x in x_test]

plt.figure(figsize=(10, 6))
plt.scatter(range(len(y_true)), y_true, color='blue', label='True Values')
plt.scatter(range(len(y_pred)), y_pred, color='red', label='Predicted Values')
plt.legend()
plt.xlabel('Index')
plt.ylabel('Value')
plt.title('True vs Predicted Values')
plt.show()
