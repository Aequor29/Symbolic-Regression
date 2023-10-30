import csv
import numpy as np
from expression_tree22 import Expression  # Make sure this is in your directory
from genetic22 import genetic_programming  # Make sure this is in your directory
from logger import initialize_log_csv, log_data, initialize_summary_csv, log_summary_data  # Make sure this is in your directory
import matplotlib.pyplot as plt

# Initialize Summary and Log CSVs
initialize_summary_csv()
initialize_log_csv()

xSet = []
ySet = []

x1a, x2a, x3a,x1b,x2b,x3b=0,0,0,1,1,1
with open('dataset2.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        x1,x2,x3, y = map(float,row)
        
        xSet.append(np.array([x1,x2,x3]))
        ySet.append(y)
xa=[min([x[0] for x in xSet]),min([x[1] for x in xSet]),min([x[2] for x in xSet])]
xb=[max([x[0] for x in xSet])-min([x[0] for x in xSet]),max([x[1] for x in xSet])-min([x[1] for x in xSet]),max([x[2] for x in xSet])-min([x[2] for x in xSet])]
x1a,x2a,x3a=xa[0],xa[1],xa[2]
x1b,x2b,x3b=xb[0],xb[1],xb[2]
xSet = np.array([np.array([(x[0]-x1a)/x1b,(x[1]-x2a)/x2b,(x[2]-x3a)/x3b]) for x in xSet])
ySet = np.array(ySet)
xeSet=[]
yeSet=[]
xtSet=[]
ytSet=[]
l1,l2,l3=0,0,0
for i in range(len(xSet)):
    if ySet[i]>0.05 and xSet[i][2]*x3b+x3a>0.05:
        xeSet.append(xSet[i])
        yeSet.append(ySet[i])
    else:
        continue
    if ySet[i]<0.62:
        if l1<100:
            ytSet.append(ySet[i])
            xtSet.append(xSet[i])
            l1+=1
    if ySet[i]>0.62 and ySet[i]<33000:
        if l2<300:
            ytSet.append(ySet[i])
            xtSet.append(xSet[i])
            l2+=1
    if ySet[i]>33000:
        if l3<100:
            ytSet.append(ySet[i])
            xtSet.append(xSet[i])
            l3+=1
# Parameters to test
max_depths = [2, 3, 4, 5]
population_sizes = [50, 100, 150, 200, 250, 300]
functions = ['+', '-', '*', '/']
terminals = ['x', 'x1', 'x2', 'x3']

# Run the experiment 30 times for each parameter setting
for max_depth in max_depths:
    for population_size in population_sizes:
        for run in range(1, 3):
            print(f"Starting run {run} with max_depth={max_depth}, population_size={population_size}")
            
            # Run Genetic Programming
            best_expression, num_generation = genetic_programming(max_depth=max_depth, size=population_size, xSet=xtSet, ySet=ytSet, functions=functions, terminals=terminals,xa=xa,xb=xb)

            # Log summary data
            best_expression_str = best_expression.print_expression(best_expression.root, xa,xb)
            log_summary_data(terminals, population_size, max_depth, best_expression_str, best_expression.exval(xeSet,yeSet), num_generation, run)

            print(f"Completed run {run}")

    
    