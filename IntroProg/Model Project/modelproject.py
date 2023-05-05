import matplotlib.pyplot as plt
import numpy as np

class ASAD:
    def __init__(self, T, z, s, alpha=0.7, gamma=0.075, tol=0.00001, z_duration=1, s_duration=1):
        self.alpha = alpha
        self.gamma = gamma
        self.tol = tol
        self.T = T
        self.z = z
        self.s = s
        self.z_duration = z_duration
        self.s_duration = s_duration

    def solve_model(self):
        self.yhat_vec = []
        self.pihat_vec = []
        self.t_vec = []

        for t in range(self.T):
            if t == 0:
                yhat = 0
                pihat = 0
            elif t <= self.z_duration or t <= self.s_duration:
                z = self.z if t <= self.z_duration else 0
                s = self.s if t <= self.s_duration else 0
                yhat = (z - self.alpha * s) / (1 + self.alpha * self.gamma)
                pihat = (self.gamma * z + s) / (1 + self.alpha * self.gamma)
            else:
                z = 0
                s = 0
                yhat = (z - self.alpha * self.pihat_vec[t - 1] - self.alpha * s) / (1 + self.alpha * self.gamma)
                pihat = (self.pihat_vec[t - 1] + self.gamma * z + s) / (1 + self.alpha * self.gamma)
                if yhat < self.tol and pihat < self.tol:
                    yhat = 0
                    pihat = 0

            self.yhat_vec.append(yhat)
            self.pihat_vec.append(pihat)
            self.t_vec.append(t)
    def plot_ad_as(self):
        y_values = np.linspace(-0.01, 0.01, 100)
        pi_hat = self.pihat_vec

        def ad_function(alpha, y, t, z, z_duration):
            if t <= z_duration:
                z_t = z
            else:
                z_t = 0
            return (-1/alpha)*(y-z_t)

        def as_function(alpha, pi_1, gamma, y, t, s, s_duration):
            if t <= s_duration:
                s_t = s
            else:
                s_t = 0
            return pi_1 + gamma * y + s_t

        # Initial equilibrium:
        LRAD = ad_function(self.alpha, y_values, 0, 0, self.z_duration)

        # Initiate plot
        plt.figure(figsize=(10, 6))
        plt.axvline(x=0, color="red", label="LRAS curve") #LRAS curve

        if self.z_duration < self.T or self.s_duration < self.T:
            # The case for short-term shocks
            for t in range(self.T):
                if t <= self.z_duration:
                    ad_curve_t = ad_function(self.alpha, y_values, t, self.z, self.z_duration)
                else:
                    ad_curve_t = ad_function(self.alpha, y_values, t, 0, self.z_duration)
                plt.plot(y_values, ad_curve_t)

            for t in range(self.T):
                if t == 0:
                    pi_1 = 0
                else:
                    pi_1 = pi_hat[t-1]
                as_curve_t = as_function(self.alpha, pi_1, self.gamma, y_values, t, self.s, self.s_duration)
                plt.plot(y_values, as_curve_t)

        else:
            # The case for permanent shocks
            # Initial LRAS
            plt.axvline(x=0, color="red", label="LRAS1 curve")

            # New LRAS (LRAS2)
            new_y = self.s / (1 + self.alpha * self.gamma)
            plt.axvline(x=new_y, color="green", label="LRAS2 curve")

            # Plot LRAD curve
            LRAD = ad_function(self.alpha, y_values, 0, 0, self.z_duration)
            plt.plot(y_values, LRAD, color="blue", label="LRAD curve")

        plt.plot(y_values, LRAD, color="blue", label="LRAD curve")
        plt.xlabel("Output gap")
        plt.ylabel("Inflation gap")
        plt.xticks([])
        plt.yticks([])
        if self.z_duration < self.T or self.s_duration < self.T:
            plt.title(f"Figure 2: {self.z_duration} period postive demand shock")
        else:
            plt.title(f"Figure 2: Permanent supply shock")
        plt.grid()
        plt.show()



