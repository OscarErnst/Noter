from scipy import optimize

class ASAD:
    def __init__(self, T, z, s, alpha=0.7, gamma=0.075, tol=0.01):
        # a) Parameter values given externally
        self.alpha = alpha  # Slope of AD
        self.gamma = gamma  # Slope of SRAS
        self.tol = tol  # Tolerance of gap variables
        # b) Modifiable parameters
        self.T = T  # Number of periods
        self.z = z  # Demand shock
        self.s = s  # Supply shock
    
    # c) Creating the solve model
    def solve_model(self):
        self.yhat_vec = []  # Vector for output gaps
        self.pihat_vec = []  # Vector for inflation gaps
        self.t_vec = []

        # d) Defining the range
        for t in range(self.T):  # Notice the "+ 1" here
            if t == 0: # Long run equilibrium
                yhat = 0 #Output gap = 0
                pihat = 0 # Inflation gap = 0
                self.yhat_vec.append(yhat) 
                self.pihat_vec.append(pihat)
                self.t_vec.append(t)
            elif t == 1: #Initial movement of the gaps after demand shock
                yhat = (self.z - self.alpha * self.s) / (1 + self.alpha * self.gamma)
                pihat = (self.gamma * self.z + self.s) / (1 + self.alpha * self.gamma)
                self.yhat_vec.append(yhat)
                self.pihat_vec.append(pihat)
                self.t_vec.append(t)
            else: # Movement until tolerance is broken
                self.z = 0
                self.s = 0
                yhat = (self.z - self.alpha * self.pihat_vec[t - 1] - self.alpha * self.s) / (1 + self.alpha * self.gamma)
                pihat = (self.pihat_vec[t - 1] + self.gamma * self.z + self.s) / (1 + self.alpha * self.gamma)
                if yhat < self.tol and pihat < self.tol:
                    break
                self.yhat_vec.append(yhat)
                self.pihat_vec.append(pihat)
                self.t_vec.append(t)
