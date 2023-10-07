import numpy as np
import random

class Node:
    def __init__(self, value, depth,left = None, right = None):
        self.value = value
        self.left = left
        self.right = right
        self.depth = depth

class Expression:
    def __init__(self, max_depth, functions, terminals):
        self.list_node=[]
        self.fitness = 0
        self.depth = 1
        self.root = Node(value=random.choice(functions), depth =0)
        self.list_node.append(self.root)

        stack = stack()
        stack.push(self.root)
        while stack:
            cur_node=stack.pop()
            if cur_node.depth==max_depth:
                continue
            if cur_node.left!= None:
                new_node= Node(random.choice(functions+terminals), cur_node.depth+1)
                self.list_node.append(new_node)
                cur_node.left=new_node
                if new_node.value in functions:
                    stack.push(new_node)
            new_node=Node(random.choice(functions+terminals), cur_node.depth+1)
            self.list_node.append(new_node)
            if new_node.value in functions:
                stack.push(new_node)

    def evaluate(self, node,x):
        if node is None:
            return 0
        left_val=self.evaluate(self, node.left, x)
        right_val=self.evaluate(self, node.right, x)
        if  node.value=='-':
            return left_val-right_val
        elif node.value=='+':
            return left_val+right_val
        elif node.value=='*':
            return left_val*right_val
        elif node.value=='/':
            if node.right == 0:
                print('divided by zero')
                return 0
            return left_val/right_val
        elif node.value=='x':
            return x
        else: 
            return node.value
    
    def __lt__(self, other):
        if self.fitness < other.fitness:
            return True
        else:
            return False

    def getfitness(self, xSet, ySet):
        yhat = np.array([self.evaluate(x) for x in xSet])
        return np.mean((ySet-yhat)**2)
    
    def muate(self):
        
        return
    
    def crossover(self):

        return

if __name__ == '__main__':
    functions = ['+', '-', '*', '/']
    termial = ['x', '1', '2', '3', '4', '5', '6', '7', '8', '9']



