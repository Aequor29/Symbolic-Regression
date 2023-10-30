import numpy as np
import matplotlib.pyplot as plt
import math

def complex_function(x):
    try:
        result = np.exp(2 - ((np.exp(((2 - (np.sin((np.sin(1)) - ((x / (6 - np.exp((np.sin(1)) - np.exp(2))))) - x)) - x) + 2 - (np.sin((x - x)) - x) + (3 / (np.log(np.cos(np.sin(x))) - np.exp(5))))) + x) / 1)) * np.sin(np.sin((x - (x - (np.exp(x) + x) - np.sin(np.sin((x - (2 - x)))))))))
        result += np.exp(2 - (x / 1)) * np.sin(np.sin((x - (3 / (2 - np.exp(5)) - x)))) * (np.sin(x) - x)
        result += np.exp(2 - (np.exp(x) + x) - np.sin(np.sin((x - (np.sin((x - (x / (x - np.exp(2)) - x))) - x)))))
        result += x / 1 - 3 - x
        result -= x
        return result
    except:
        return np.nan

# Generate x values
x_values = np.linspace(-10, 10, 1000)

# Compute y values based on the complex function
y_values = [complex_function(x) for x in x_values]

# Plot the function
plt.plot(x_values, y_values)
plt.title("Plot of the Complex Function")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.show()
