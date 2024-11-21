"""
Lakota Dolce
Project 2
November 8, 2024
Dr. Debendra
"""

import numpy as np
import matplotlib.pyplot as plt

"""
Desc: This method will take in the requirement to calculate Eulers method and output the given estimation
Param: Xo -> the initial X value
Param: f -> the function used 
Param: h -> the step of the function
Param: stop -> the value to stop at
Return: value ->the float of the estimation 
"""
def EulersMethod(Xo, h, stop):
    #Initialize variables
    value = Xo
    t = 0
    #Create loop to get estimation
    while t < stop:
        #Change x for the next calculation
        value = value + f(t, value) * h
        #increment step
        t += h
    #return estimation
    return value

"""
Desc: This method will take in the requirement to calculate RK4 method and output the given estimation
Param: Xo -> the initial X value
Param: f2 -> the function used 
Param: h -> the step of the function
Param: stop -> the value to stop at
Return: value ->the float of the estimation 
"""
def RK4Method(Xo, h, stop):
    #Initialize
    X = Xo
    t = 0
    #while t is less than stop continue updating values
    while t < stop:
        #Get K values
        K1 = h * f(t, X)
        K2 = h * f(t + h/2, X + K1/2)
        K3 = h * f(t + h/2, X + K2/2)
        K4 = h * f(t + h, X + K3)
        #Calculate X
        X += (K1 + 2*K2 + 2*K3 + K4) / 6
        t += h
    #Return the value
    return X

"""
Desc: This method will take in an x value and run it through a specific function returning y
Param: X -> the x value
Return: the value after the function at x
"""
def f(x, P):
    #Calculate the value
    return 9 - 300 * (P / 800)

#Q3: Calculate the polution using Eulers Method
#initialize variables
n = 10
# 20 minutes  = 1/3 hour
b = 1/3
a = 0
#100oz in 800 gal
Xo = 100/800

#calculate h
h = (b-a)/n

#Calculate using Eulers method
print(f"Using Eulers Method we get {round(EulersMethod(Xo, h, b), 6)}")


#Q4: Calculate the polution using RK4 method

n = 10
# 20 minutes  = 1/3 hour
b = 1/3
a = 0
#100oz in 800 gal
Xo = 100/800

#calculate h
h = (b-a)/n

#Calculate using RK4 Method
print(f"Using the RK4 Method we get {round(RK4Method(Xo, h, b), 6)}")

#Q6: Prove with graph the amount of polution at t = infinity
#Initializing
n = 10
# 20 minutes  = 1/3 hour
b = 1/3
a = 0
#100oz in 800 gal
X = 0
Y = 100/800
t = 0

def pollution_rate(P):
    return  1755/24 * np.exp((-1/8 * P)) + 73/3

# Generate a range of P values (pollution levels) for the x-axis
t_values = np.linspace(0, 200, 100)  # P values from 0 to 200

# Calculate dP/dt for each value of P
P_values = pollution_rate(t_values)

# Plotting the function dP/dt = 9 - (3/800) * P
plt.figure(figsize=(10, 6))
plt.plot(t_values, P_values, label="-1755/24e^(-1/8t) + 73/3", color="b")
plt.xlabel("Pollution (P) in ounces")
plt.ylabel("Rate of Change of Pollution (P) in ounces/hour")
plt.title("Rate of Change of Pollution in the Tank")
plt.axhline(0, color="black", linestyle="--")  # Add horizontal line at dP/dt = 0 for reference
plt.grid()
plt.legend()
plt.show()