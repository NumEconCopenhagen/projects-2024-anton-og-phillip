from types import SimpleNamespace

class ExchangeEconomyClass:

    def __init__(self):

        par = self.par = SimpleNamespace()

        #Define parameters and endowments
        par.alpha = 1/3
        par.beta = 2/3
        par.w1A = 0.8
        par.w2A = 0.3
        par.w1B = 0.2
        par.w2B = 0.7
        par.p2 = 1


#Define utility function for consumer A
    def utility_A(self,x1A,x2A):

        par = self.par
        return (x1A**par.alpha)*(x2A**(1-par.alpha))


#Define utility function for consumer B
    def utility_B(self,x1B,x2B):

        par = self.par
        return (x1B**par.beta)*(x2B**(1-par.beta))

#Define demand for good 1 for consumer A
    def demand_A1(self,p1):

        par = self.par
        return par.alpha((p1*par.w1A+par.p2*par.w2A)/p1)

    #Define demand for good 2 for consumer A
    def demand_A2(self,p1):

        par = self.par
        return (1-par.alpha)((p1*par.w1A+par.p2*par.w2A)/par.p2)

#Define demand for good 1 for consumer B
    def demand_B1(self,p1):

        par = self.par
        return par.beta*((p1*par.w1B+par.p2*par.w2B)/p1)

#Define demand for good 2 for consumber B
    def demand_B2(self,p1):

        par = self.par
        return (1-par.beta)*((p1*par.w1B+par.p2*par.w2B)/par.p2)