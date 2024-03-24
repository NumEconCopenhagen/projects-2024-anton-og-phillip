import numpy as np

# Set the number of vectors
num_samples = 50

# Generate random endowment vectors for agent A
endowments_A = np.random.rand(num_samples, 2)

# Calculate endowments for agent B
endowments_B = 1 - endowments_A

# Combine endowments for agent A and agent B into a single set W
endowments_W = np.concatenate((endowments_A, endowments_B), axis=1)

# Print the set W
print("Set W (Endowments for Agent A of Good 1 and Good 2, and Endowments for Agent B of Good 1 and Good 2):")
print(endowments_W)

# Given parameters
alpha_A = 1/3
alpha_B = 2/3
price_good2 = 1  # Price of good 2

# Utility and demand functions for agent A
def utility_A(x1, x2):
    return x1**alpha_A * x2**(1-alpha_A)

def demand_A(p1, p2, omega_A1, omega_A2):
    x1 = alpha_A * omega_A1 / p1
    x2 = (1 - alpha_A) * omega_A2 / p2
    return x1, x2

# Utility and demand functions for agent B
def utility_B(x1, x2):
    return x1**alpha_B * x2**(1-alpha_B)

def demand_B(p1, p2, omega_B1, omega_B2):
    x1 = alpha_B * omega_B1 / p1
    x2 = (1 - alpha_B) * omega_B2 / p2
    return x1, x2

# Market allocation function for both agents
def market_allocation(p1, p2, omega_A1, omega_A2):
    x1_A, x2_A = demand_A(p1, p2, omega_A1, omega_A2)
    x1_B, x2_B = demand_B(p1, p2, 1 - omega_A1, 1 - omega_A2)  # Endowments for agent B are 1 - endowments for agent A
    
    # Ensure total amount of each good is 1
    total_good1 = x1_A + x1_B
    total_good2 = x2_A + x2_B
    scaling_factor = 1 / max(total_good1, total_good2)
    x1_A *= scaling_factor
    x1_B *= scaling_factor
    x2_A *= scaling_factor
    x2_B *= scaling_factor
    
    # Ensure utility for each agent is at least the same as in the original endowment
    if utility_A(x1_A, x2_A) < utility_A(omega_A1, omega_A2):
        x1_A, x2_A = omega_A1, omega_A2
    if utility_B(x1_B, x2_B) < utility_B(1 - omega_A1, 1 - omega_A2):
        x1_B, x2_B = 1 - omega_A1, 1 - omega_A2

    return x1_A, x2_A, x1_B, x2_B

# Solve for market allocations for each endowment vector in set W
market_allocations = []
for endowment in endowments_W:
    # Set p2 = 1
    p2 = 1
    
    # Initial guess for p1
    p1_guess = 1
    
    # Define the market clearing condition function
    def market_clearing_condition(p1):
        x1_A, x2_A, _, _ = market_allocation(p1, p2, endowment[0], endowment[1])
        return x1_A + endowment[0] - 1  # Market clearing condition
    
    # Solve for p1 using fsolve
    from scipy.optimize import fsolve
    p1_solution = fsolve(market_clearing_condition, p1_guess)
    
    # Calculate market allocation using the solved p1
    x1_A, x2_A, x1_B, x2_B = market_allocation(p1_solution[0], p2, endowment[0], endowment[1])
    
    # Append market allocation to the list
    market_allocations.append([x1_A, x2_A, x1_B, x2_B])

# Convert market allocations to NumPy array
market_allocations = np.array(market_allocations)

import matplotlib.pyplot as plt
import numpy as np

# Extract market allocations for each agent
x1_A = market_allocations[:, 0]
x2_A = market_allocations[:, 1]
x1_B = market_allocations[:, 2]
x2_B = market_allocations[:, 3]

# Determine the number of vectors
num_vectors = len(x1_A)

# Generate a colormap with a color for each vector
colors = plt.cm.viridis(np.linspace(0, 1, num_vectors))

# Plotting Edgeworth box
plt.figure(figsize=(8, 8))
plt.xlabel("Good 1 A")
plt.ylabel("Good 2 A")
plt.title("Edgeworth Box")

# Plot market allocations for agent A
for i in range(num_vectors):
    plt.scatter(x1_A[i], x2_A[i], color=colors[i], label=f'Agent A - Vector {i}')

# Plot market allocations for agent B (inverted axes)
for i in range(num_vectors):
    plt.scatter(1 - x1_B[i], 1 - x2_B[i], color=colors[i], label=f'Agent B - Vector {i}')

# Set axis limits to ensure axes go from 0 to 1
plt.xlim(0, 1)
plt.ylim(0, 1)

# Plot axes
plt.plot([0, 1], [0, 0], color='black')  # x-axis
plt.plot([0, 0], [0, 1], color='black')  # y-axis
plt.plot([1, 1], [0, 1], color='black')  # Second x-axis for Agent B
plt.plot([0, 1], [1, 1], color='black')  # Second y-axis for Agent B

# Add right and top axes
plt.gca().yaxis.set_label_position("right")
plt.gca().xaxis.set_label_position("top")
plt.gca().yaxis.tick_right()
plt.gca().xaxis.tick_top()
plt.xlabel("Good 1 B")
plt.ylabel("Good 2 B")

plt.grid(True)
plt.show()