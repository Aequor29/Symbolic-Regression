import csv
import numpy as np
from expression_tree import Expression  # Make sure this is in your directory
from genetic import genetic_programming  # Make sure this is in your directory
from logger import initialize_log_csv, log_data, initialize_summary_csv, log_summary_data  # Make sure this is in your directory
import matplotlib.pyplot as plt

# Initialize Summary CSV
initialize_summary_csv()
initialize_log_csv()
# Parameters to test
max_depths = [2, 3, 4, 5]
population_sizes = [50, 100, 150, 200, 250, 300]
terminal_sets = [['x', 1], ['x', 1, 2], ['x', 1, 2, 3], ['x', 1, 2, 3, 4]]
functions = ['+', '-', '*', '/'] 

# Run the experiment 30 times for each parameter setting
for max_depth in max_depths:
    for population_size in population_sizes:
        for terminals in terminal_sets:
            for run in range(1, 5):
                print(f"Starting run {run} with max_depth={max_depth}, population_size={population_size}, terminals={terminals}")

                # Load dataset
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

                # Randomly select 3000 points
                if len(xSet) >= 3000:
                    random_indices = np.random.choice(len(xSet), 3000, replace=False)
                    xtSet = xSet[random_indices]
                    ytSet = ySet[random_indices]
                else:
                    print("Dataset has fewer than 3000 points, using all available points for training.")
                

                # Run Genetic Programming
                best_expression, num_generation = genetic_programming(max_depth=max_depth, size=population_size, xSet=xtSet, ySet=ytSet, functions=functions, terminals=terminals)

                # Log summary data
                best_expression_str = best_expression.print_expression(best_expression.root)
                log_summary_data(terminals, population_size, max_depth, best_expression_str, best_expression.eval(xSet,ySet), num_generation,run)

                print(f"Completed run {run}")

                # Optional: Plotting (You may want to comment this out when running many experiments)
                # ...

