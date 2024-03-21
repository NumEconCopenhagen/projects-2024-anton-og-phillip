from scipy import optimize 
# Define alpha and beta
alpha = 1/3
beta = 2/3

# Define endowment points
omega_A1 = 0.8
omega_A2 = 0.3
omega_B1 = 1 - omega_A1
omega_B2 = 1 - omega_A2

N = 75

p2 = 1
P1 = [0.5+2*i/N for i in range(N+1)]

def 


# Define utility functions
def u_A(p1):
    x_A1 = alpha * (p1 * omega_A1 + omega_A2 * p2) / p1
    x_A2 = (1 - alpha) * (p1 * omega_A1 + omega_A2 * p2) / p2
    

    return x_A1**alpha*x_A2**(1-alpha)

#define objection function
def  objection_A(p1):
    return -u_A(p1)

#define bound so p1 is in P1
bounds = [0.5, 2.5]

def optimal_choice_A():
    optimize.minimize_scalar(u_A, bounds=bounds, method = "bounded")




   





       


