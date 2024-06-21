import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interactive, FloatSlider
# Create model setup
# Parameters
wage = 1.0  # Wage when young
interest_rate = 0.04  # Initial interest rate
beta = 0.96  # Initial discount factor
num_iterations = 100  # Number of iterations for the algorithm
tolerance = 1e-6  # Convergence tolerance

# Utility function: log utility
def utility(c):
    return np.log(c)

# Objective function for young agents
def objective_savings(s, wage, interest_rate, beta):
    c_y = wage - s  # Consumption while young
    c_o = (1 + interest_rate) * s  # Consumption while old
    
    if c_y <= 0 or c_o <= 0:
        return -np.inf  # Invalid consumption levels
    
    # Total utility: current utility + discounted future utility
    total_utility = utility(c_y) + beta * utility(c_o)
    return total_utility


# Iterative algorithm to find optimal savings
def find_optimal_savings(wage, interest_rate, beta):
    num_iterations = 100  # Number of iterations for the algorithm
    tolerance = 1e-6  # Convergence tolerance
    s_lower, s_upper = 0.01, wage  # Set search bounds for savings
    for _ in range(num_iterations):
        s_mid = (s_lower + s_upper) / 2.0
        grad_left = (objective_savings(s_lower, wage, interest_rate, beta) - 
                     objective_savings(s_mid, wage, interest_rate, beta)) / (s_mid - s_lower)
        grad_right = (objective_savings(s_upper, wage, interest_rate, beta) - 
                      objective_savings(s_mid, wage, interest_rate, beta)) / (s_upper - s_mid)
        
        # Determine which direction to adjust bounds
        if grad_left > grad_right:
            s_upper = s_mid
        else:
            s_lower = s_mid
        
        # Check for convergence
        if abs(s_upper - s_lower) < tolerance:
            break
    
    optimal_savings = (s_lower + s_upper) / 2.0
    optimal_consumption_young = wage - optimal_savings
    optimal_consumption_old = (1 + interest_rate) * optimal_savings
    return optimal_savings, optimal_consumption_young, optimal_consumption_old

# Print and plot the optimal savings solution for different parameter values
def plot_savings_solution():
    wage = 1.0  # Wage when young
    beta = 0.96  # Initial discount factor
    betas = [0.90, 0.96, 1.02]  # Range of discount factors
    interest_rates = [0.02, 0.04, 0.06]  # Range of interest rates
    
    fig, axs = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot for discount factors
    for b in betas:
        optimal_s, c_y, c_o = find_optimal_savings(wage, 0.04, b)  # Using a fixed interest rate for beta comparison
        axs[0].plot([b], [optimal_s], 'o', label=f'Beta={b}')
        print(f'Beta={b}: Optimal Savings={optimal_s:.4f}, Young Consumption={c_y:.4f}, Old Consumption={c_o:.4f}')
    axs[0].set_xlabel('Discount Factor (Beta)')
    axs[0].set_ylabel('Optimal Savings')
    axs[0].legend()
    axs[0].set_title('Optimal Savings vs. Discount Factor')
    
    # Plot for interest rates
    for r in interest_rates:
        optimal_s, c_y, c_o = find_optimal_savings(wage, r, 0.96)  # Using a fixed beta for interest rate comparison
        axs[1].plot([r], [optimal_s], 'o', label=f'Interest Rate={r}')
        print(f'Interest Rate={r}: Optimal Savings={optimal_s:.4f}, Young Consumption={c_y:.4f}, Old Consumption={c_o:.4f}')
    axs[1].set_xlabel('Interest Rate')
    axs[1].set_ylabel('Optimal Savings')
    axs[1].legend()
    axs[1].set_title('Optimal Savings vs. Interest Rate')
    
    plt.tight_layout()
    plt.show()

    # CRRA Utility Function
def utility_crra(c, gamma):
    if c <= 0:
        return -np.inf
    if gamma == 1:
        return np.log(c)  # Special case: logarithmic utility
    else:
        return (c**(1 - gamma) - 1) / (1 - gamma)

# Objective function for young agents with CRRA utility
def objective_savings_crra(s, wage, interest_rate, beta, gamma):
    c_y = wage - s  # Consumption while young
    c_o = (1 + interest_rate) * s  # Consumption while old
    
    if c_y <= 0 or c_o <= 0:
        return -np.inf  # Invalid consumption levels
    
    # Total utility: current + discounted future
    total_utility = utility_crra(c_y, gamma) + beta * utility_crra(c_o, gamma)
    return total_utility

# Finding optimal savings with the CRRA utility
def find_optimal_savings_crra(wage, interest_rate, beta, gamma):
    s_lower, s_upper = 0.01, wage  # Search bounds
    num_iterations = 100
    tolerance = 1e-6
    
    while s_upper - s_lower > tolerance:
        s_mid = (s_lower + s_upper) / 2.0
        grad_left = (objective_savings_crra(s_lower, wage, interest_rate, beta, gamma) - 
                     objective_savings_crra(s_mid, wage, interest_rate, beta, gamma)) / (s_mid - s_lower)
        grad_right = (objective_savings_crra(s_upper, wage, interest_rate, beta, gamma) - 
                      objective_savings_crra(s_mid, wage, interest_rate, beta, gamma)) / (s_upper - s_mid)
        
        if grad_left > grad_right:
            s_upper = s_mid
        else:
            s_lower = s_mid

    optimal_savings = (s_lower + s_upper) / 2.0
    return optimal_savings, wage - optimal_savings, (1 + interest_rate) * optimal_savings

# Visualize optimal savings for different levels of risk aversion (gamma)
def plot_savings_crra():
    wage = 1.0
    interest_rate = 0.04
    beta = 0.96
    gammas = [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]  # Different levels of risk aversion (gamma)
    
    optimal_savings_values = []
    print("Gamma, Optimal Savings, Young Consumption, Old Consumption")
    for gamma in gammas:
        optimal_s, c_y, c_o = find_optimal_savings_crra(wage, interest_rate, beta, gamma)
        optimal_savings_values.append(optimal_s)
        print(f"{gamma:.1f}, {optimal_s:.4f}, {c_y:.4f}, {c_o:.4f}")
    
    plt.figure(figsize=(10, 6))
    plt.plot(gammas, optimal_savings_values, marker='o')
    plt.xlabel('Risk Aversion (Gamma)')
    plt.ylabel('Optimal Savings')
    plt.title('Optimal Savings vs. Risk Aversion')
    plt.grid(True)
    plt.show()

    # Visualize optimal savings for different interest rates with a fixed CRRA gamma value
def plot_savings_interest_rate(gamma):
    wage = 1.0
    beta = 0.96
    interest_rates = np.linspace(0.01, 0.1, 10)  # Interest rate range from 0.01 to 0.1
    
    print("Interest Rate, Optimal Savings, Young Consumption, Old Consumption")
    optimal_savings_values = []
    for r in interest_rates:
        optimal_s, c_y, c_o = find_optimal_savings_crra(wage, r, beta, gamma)
        optimal_savings_values.append(optimal_s)
        print(f"{r:.2f}, {optimal_s:.4f}, {c_y:.4f}, {c_o:.4f}")
    
    plt.figure(figsize=(8, 6))
    plt.plot(interest_rates, optimal_savings_values, marker='o')
    plt.xlabel('Interest Rate')
    plt.ylabel('Optimal Savings')
    plt.title(f'Optimal Savings vs. Interest Rate (Gamma = {gamma})')
    plt.grid(True)
    plt.show()

# Function to plot the results
def plot_olg_model(wage, interest_rate, beta, gamma):
    optimal_savings, consumption_young, consumption_old = find_optimal_savings_crra(wage, interest_rate, beta, gamma)
    
    labels = ['Young', 'Old']
    consumption_values = [consumption_young, consumption_old]
    
    plt.figure(figsize=(10, 6))
    plt.bar(labels, consumption_values, color=['skyblue', 'lightgreen'])
    plt.title(f'Consumption when Young and Old (gamma={gamma}, beta={beta}, interest_rate={interest_rate})')
    plt.ylabel('Consumption')
    plt.ylim(0, wage)
    
    for i, value in enumerate(consumption_values):
        plt.text(i, value + 0.05 * wage, f'{value:.2f}', ha='center')
    
    plt.show()

# Interactive widget
interactive_plot = interactive(
    plot_olg_model,
    wage=FloatSlider(value=1000, min=500, max=2000, step=50, description='Wage'),
    interest_rate=FloatSlider(value=0.05, min=0.01, max=0.9, step=0.01, description='Interest Rate'),
    beta=FloatSlider(value=0.95, min=0.1, max=1.0, step=0.01, description='Beta'),
    gamma=FloatSlider(value=2, min=0.1, max=6, step=0.1, description='Gamma')
)

# Display the interactive plot
interactive_plot

