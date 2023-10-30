import csv
import numpy as np
from genetic22 import*
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
    if ySet[i]>0.3 and xSet[i][2]*x3b+x3a>0.3:
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
# Parameters
terminals = ['x', 'x1','x2','x3']
functions = ['+', '-', '*', '/']
max_depth = 5
population_size = 350

best_expression = genetic_programming(max_depth=max_depth, size=population_size, xSet=xtSet, ySet=ytSet, functions= functions, terminals= terminals,xa=xa,xb=xb)
best_eval=best_expression.exeval(xeSet,yeSet)
txtime=time.perf_counter()
print(txtime)
print(best_eval)
for i in range(500):
    new_best=genetic_programming(max_depth=max_depth, size=population_size, xSet=xtSet, ySet=ytSet, functions= functions, terminals= terminals,xa=xa,xb=xb)
    now_eval=new_best.exeval(xeSet,yeSet)
    
    if now_eval<best_eval:
        best_expression=new_best
        best_eval=now_eval
    print('which round')
    print(i)
    timeused=time.perf_counter()-txtime
    txtime=time.perf_counter()
    print('timeused:')
    print(timeused)
    print(now_eval)
    
    print("Best Expression:", best_expression.print_expression(best_expression.root,xa,xb))
    print("Best Fitness:", best_expression.fitness)
    print("Best Eval:", best_eval)
    if txtime-time1>3600:
        break
    
    
    
print("Best Expression:", best_expression.print_expression(best_expression.root,xa,xb))
print("Best Fitness:", best_expression.fitness)
print("Best Eval:", best_eval)

time2=time.perf_counter()
print(time2-time1)