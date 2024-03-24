from scipy.optimize import minimize_scalar 
import numpy as np

# Define alpha and beta
alpha = 1/3
beta = 2/3

# Define endowment points
omega_A1 = 0.8
omega_A2 = 0.3
omega_B1 = 1 - omega_A1
omega_B2 = 1 - omega_A2

#Set p2 to 1
p2 = 1


# Define utility function for A
def u_A(p1):
    x_A1 = alpha * (p1 * omega_A1 + omega_A2 * p2) / p1
    x_A2 = (1 - alpha) * (p1 * omega_A1 + omega_A2 * p2) / p2

    return x_A1**alpha*x_A2**1-alpha, x_A1, x_A2

#paramters for generating the set P1
starting_point = 0.5
N = 75

#Define the set (P1 in the assignment text) that contains the elements of values that p1 can take
Possible_Prices = [starting_point + 2*(i/N) for i in range(N)]

#Calculate the utility asscociated with each element of the set of possible prices and find the maximum value
max_utility = -float("inf")
best_p1 = None
for p1 in Possible_Prices:
    utility = u_A(p1)[0]
    if utility > max_utility:
        if (u_A(p1)[1] or u_A(p1)[2]) <= 1:
            max_utility = utility
            best_p1 = p1


print("Maximum utility:", max_utility)
print("Best p1:", best_p1)


#Demand functions for consumer A given chosen price
x_A1 = alpha * (p1 * omega_A1 + omega_A2 * p2) / p1
x_A2 = (1 - alpha) * (p1 * omega_A1 + omega_A2 * p2) / p2

p1 = 2.4733333333333336

print("Amount of good 1 for A:", x_A1)
print("Amount of good 2 for A:", x_A2)


    
    





   





       


