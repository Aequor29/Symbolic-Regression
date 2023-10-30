import csv

def initialize_log_csv():
    with open('experiment1_data.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Generation', 'Best_Fitness', 'Terminals', 'Population_Size', 'Max_Depth'])

def log_data(generation, best_fitness,terminals, population_size, max_depth):
    with open('experiment1_data.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([generation, best_fitness,terminals, population_size, max_depth])

def initialize_summary_csv():
    with open('experiment1_summary.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['terminals','population_size', 'max_depth' ,'experssion' ,'eval', 'num_of_gen','num_of_runs'])

def log_summary_data(terminals, population_size, max_depth, expression, eval, num_gen,num_of_runs):
    with open('experiment1_summary.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([terminals, population_size, max_depth, expression, eval, num_gen,num_of_runs])
