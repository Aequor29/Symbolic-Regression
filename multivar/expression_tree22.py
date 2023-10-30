from collections import deque
import copy
import math
import numpy as np
import random

class Node:
    def __init__(self,value,left = None, right = None):
        self.value = value
        if value=='x':
            self.value=10*random.random()
        self.left = left
        self.right = right

class Expression:

    def __init__(self, max_depth,functions, terminals, xSet, ySet):
        self.xSet = np.array(xSet)
        self.ySet = np.array(ySet)
        self.functions = functions
        self.terminals = terminals
        self.list_terminals = []
        self.list_node=[]
        self.variables=['x1','x2','x3']
        self.max_depth=max_depth
        
        self.root = Node(value=random.choice(functions))
        self.list_node.append(self.root)
        self.depth = 0
        self.max_depth=max_depth
        stack = deque()
        stack.append(self.root)
        while stack:
            node = stack.pop()
            if node.value in functions:
                if self.depth < max_depth:
                    node.left = Node(value=random.choice(functions+terminals))
                    node.right = Node(value=random.choice(functions+terminals))
                    stack.append(node.right)
                    stack.append(node.left)
                    self.list_node.append(node.left)
                    self.list_node.append(node.right)
                    self.depth += 1
                else: 
                    node.left = Node(value=random.choice(terminals))
                    node.right = Node(value=random.choice(terminals))
                    self.depth += 1
            else:
                node.left = None
                node.right = None
                self.list_terminals.append(node)

        self.fitness = self.getfitness()

    def evaluate(self, node,x):
        if node is None:
            return 0
        left_val=self.evaluate(node.left, x)
        right_val=self.evaluate(node.right, x)
        if  node.value=='-':
            return left_val-right_val
        elif node.value=='+':
            return left_val+right_val
        elif node.value=='*':
            return left_val*right_val
        elif node.value=='/':
            if right_val == 0:
                add_node=Node(0.00000001)
                new_node=Node('+',node.right,add_node)
                node.right=new_node
                right_val=self.evaluate(node.right,x)
            return left_val/right_val
        elif node.value=='x1':
            return x[0]
        elif node.value=='x2':
            return x[1]
        elif node.value=='x3':
            return x[2]
        else: 
            return float(node.value)
    
    def __lt__(self, other):
        if self.fitness < other.fitness:
            return True
        else:
            return False

    def getfitness(self):
        yhat = np.array([self.evaluate(self.root,x) for x in self.xSet])
        return np.mean(np.sqrt((yhat/self.ySet *100-100)**2))*math.log(self.depth+8)
    
    def exval(self,xeSet,yeSet):
        yhat = np.array([self.evaluate(self.root,x) for x in xeSet])
        return np.mean(np.sqrt((yhat/yeSet *100-100)**2))*math.log(self.depth+8)
    
    def update(self):
        self.fitness = self.getfitness()
        self.fitness = self.getfitness()
        self.list_terminals =[]
        self.list_node=[]
        stack = deque()
        self.depth=0
        stack.append(self.root)
        while stack:
            node = stack.pop()
            self.list_node.append(node)
            if node.value in self.functions:
                stack.append(node.right)
                stack.append(node.left)
                self.depth+=1
            else :
                self.list_terminals.append(node)

    def mutate(self):
        child = copy.deepcopy(self)
        new_ex=Expression(self.max_depth,self.functions,self.terminals,self.xSet,self.ySet)
        random_node = random.choice(child.list_node)
        #if random_node.value in self.variables:
            #random_node.value = random.choice(self.constants)
        #else:
            #random_node.value = random.choice(self.variables)
        random_node.value=new_ex.root.value
        random_node.left=new_ex.root.left
        random_node.right=new_ex.root.right
        child.update()
        return child
    
    def crossover(self, other):
        child1 = copy.deepcopy(self)
        child2 = copy.deepcopy(other)

        random_node1 = random.choice(child1.list_node)
        random_node2 = random.choice(child2.list_node)

        random_node1.value, random_node2.value = random_node2.value, random_node1.value
        random_node1.left, random_node2.left = random_node2.left, random_node1.left
        random_node1.right, random_node2.right = random_node2.right, random_node1.right

        child1.update()
        child2.update()
        
        return child1, child2
    
    def print_expression(self, node,xa,xb):
        
        if node is None:
            return ""
        if node.value in self.functions:
            left = self.print_expression(node.left,xa,xb)
            right = self.print_expression(node.right,xa,xb)
            return f"({left} {node.value} {right})"
        elif node.value=='x1':
            return f"((x1-{xa[0]})/{xb[0]})"
        elif node.value=='x2':
            return f"((x2-{xa[1]})/{xb[1]})"
        elif node.value=='x3':
            return f"((x3-{xa[2]})/{xb[2]})"
        else:
            return node.value