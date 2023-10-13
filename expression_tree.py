from collections import deque
import copy
import math
import numpy as np
import random

class Node:
    def __init__(self,value,left = None, right = None):
        self.value = value
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
        self.constants= [t for t in terminals if t != 'x']
        self.root = Node(value=random.choice(functions))
        self.list_node.append(self.root)
        self.depth = 1  

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
            elif node.value in terminals:
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
                return 0
            return left_val/right_val
        elif node.value=='x':
            return x
        else: 
            return float(node.value)
    
    def __lt__(self, other):
        if self.fitness < other.fitness:
            return True
        else:
            return False

    def getfitness(self):
        yhat = np.array([self.evaluate(self.root,x) for x in self.xSet])
        return np.mean((self.ySet-yhat)**2)*math.log(math.log(self.depth+2)+3)
    
    def update(self):
        self.fitness = self.getfitness()
        self.list_terminals =[]
        stack = deque()
        stack.append(self.root)
        while stack:
            node = stack.pop()
            if node.value in self.functions:
                stack.append(node.right)
                stack.append(node.left)
            elif node.value in self.terminals:
                self.list_terminals.append(node)

    def mutate(self):
        child = copy.deepcopy(self)

        random_node = random.choice(child.list_terminals)
        if random_node.value == 'x':
            random_node.value = random.choice(self.constants)
        else:
            random_node.value = 'x'

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
    
    def print_expression(self, node):
        if node is None:
            return ""
        if node.value in ['+', '-', '*', '/']:
            left = self.print_expression(node.left)
            right = self.print_expression(node.right)
            return f"({left} {node.value} {right})"
        else:
            return node.value




