"""
Lakota Dolce
Math 242
Lab 8
Dr. Debendra
"""

import numpy as np
import matplotlib.pyplot as plt

""" Eulers Method
desc: This is a function to calculate the Eulers method and return a value at time (t)
param: Xo - the initial X value
param: Yo - the initial y value
param: h - the step size of the function
param: b - the end location of the function
param: a- the start location
return: value - a value calculated using Eulers method at a time (t)
"""

def EulersMethod(a, b, h, X, Y, f):
    return Y + h * f(X, Y)


""" RK4 Method
desc: This is a function to use the RK4 method to return an estimation at time (t)
param: X - The x value
param: Y - the y value
param: h - the step size of the function
return: int value of after calculating the RK4 method
"""
def RK4Method(h, X, Y, f):
    #Get K values
    K1 = f(X, Y)
    K2 =  f(X + h/2, Y + h*K1/2)
    K3 =  f(X + h/2, Y + h*K2/2)
    K4 =  f(X + h, Y + h*K3)
    #Return the value
    return Y + h/6 * (K1 + 2*K2 + 2*K3 + K4)



#Question 1
def Q1a():
    # 1a)
    """
    desc: The function that we are estimating
    param: x - the x value
    param: y - the y value
    return: int value after x and y are substituted for the calculation
    """
    def fa(x, y):
        return 3 - 2* x - 1/2 * y
    
    def exactf(x):
        return 14 - 4 * x - 13 * np.exp(-x / 2)
    #Initialize
    a = 0
    b = 2
    n1 = 20
    n2 = 40
    n3 = 200
    h1 = (b-a)/n1
    h2 = (b-a)/n2
    h3 = (b-a)/n3
    Yo = 1
    XValues1 = np.linspace(0, 2, n1+1)
    XValues2 = np.linspace(0, 2, n2+1)
    XValues3 = np.linspace(0, 2, n3+1)
    YValues1 = np.zeros(n1+1)
    YValues2 = np.zeros(n2+1)
    YValues3 = np.zeros(n3+1)
    exactXValues = np.linspace(0,2,200)
    exactYValues = exactf(exactXValues)
    YValues1[0] = YValues2[0] = YValues3[0] = exactYValues[0] = Yo

    #Get the Y values at X
    for i in range(len(XValues3)-1):
        if i < n1:
            YValues1[i+1] = EulersMethod(a, b, h1, XValues1[i], YValues1[i], fa)
        if i < n2:
            YValues2[i+1] = EulersMethod(a, b, h2, XValues2[i], YValues2[i], fa)
        if i < n3:
            YValues3[i+1] = EulersMethod(a, b, h3, XValues3[i], YValues3[i], fa)
    
    #Plot
    plt.plot(exactXValues, exactYValues, 'k--', label='Exact Solution')
    plt.plot(XValues1, YValues1, 'r--', label = "Euler h=.1")
    plt.plot(XValues2, YValues2, 'b--', label = "Euler h=.05")
    plt.plot(XValues3, YValues3, 'g--', label = "Euler h=.01")
    plt.legend()
    plt.xlabel('t')
    plt.ylabel('y')
    plt.title("Aproximation Solution vs Exact Solution")
    plt.grid(True)
    plt.show()
    return

def Q1b():
    # 1b)
    """
    desc: The function that we are estimating
    param: x - the x value
    param: y - the y value
    return: int value after x and y are substituted for the calculation
    """
    def fb(x, y):
        return 4 - x + 2 * y
    
    def exactf(x):
        return -7/4 + 1/2 * x + 11/4 * np.exp(2*x)
    #Initialize
    a = 0
    b = 2
    n1 = 20
    n2 = 40
    n3 = 200
    h1 = (b-a)/n1
    h2 = (b-a)/n2
    h3 = (b-a)/n3
    Yo = 1
    XValues1 = np.linspace(0, 2, n1+1)
    XValues2 = np.linspace(0, 2, n2+1)
    XValues3 = np.linspace(0, 2, n3+1)
    YValues1 = np.zeros(n1+1)
    YValues2 = np.zeros(n2+1)
    YValues3 = np.zeros(n3+1)
    exactXValues = np.linspace(0,2,200)
    exactYValues = exactf(exactXValues)
    YValues1[0] = YValues2[0] = YValues3[0] = exactYValues[0] = Yo

    #Get the Y values at X
    for i in range(len(XValues3)-1):
        if i < n1:
            YValues1[i+1] = EulersMethod(a, b, h1, XValues1[i], YValues1[i], fb)
        if i < n2:
            YValues2[i+1] = EulersMethod(a, b, h2, XValues2[i], YValues2[i], fb)
        if i < n3:
            YValues3[i+1] = EulersMethod(a, b, h3, XValues3[i], YValues3[i], fb)
    
    #Plot
    plt.plot(exactXValues, exactYValues, 'k--', label='Exact Solution')
    plt.plot(XValues1, YValues1, 'r--', label = "Euler h=.1")
    plt.plot(XValues2, YValues2, 'b--', label = "Euler h=.05")
    plt.plot(XValues3, YValues3, 'g--', label = "Euler h=.01")
    plt.legend()
    plt.xlabel('t')
    plt.ylabel('y')
    plt.title("Aproximation Solution vs Exact Solution")
    plt.grid(True)
    plt.show()
    return

def Q2a():
    """
    desc: The function that we are estimating
    param: x - the x value
    param: y - the y value
    return: int value after x and y are substituted for the calculation
    """
    def fa(x, y):
        return 3 - 2* x - 1/2 * y
    
    def exactf(x):
        return 14 - 4 * x - 13 * np.exp(-x / 2)
    
    #Initialize
    a = 0
    b = 2
    h = .2
    n = int((b-a)/h)
    Yo = 1
    XValuesE = np.linspace(0, 2, n+1)
    XValuesR = np.linspace(0, 2, n+1)
    YValuesE = np.zeros(n+1)
    YValuesR = np.zeros(n+1)
    YValuesE[0] = YValuesR[0] = Yo
    exactXValues = np.linspace(0,2,200)
    exactYValues = exactf(exactXValues)

#Get the Y values at X
    for i in range(10):
        YValuesE[i+1] = EulersMethod(a, b, h, XValuesE[i], YValuesE[i], fa)
        YValuesR[i+1] = RK4Method(h, XValuesR[i], YValuesR[i], fa)
    
    #Plot
    plt.plot(exactXValues, exactYValues, 'g--', label='Exact Solution')
    plt.plot(XValuesR, YValuesR, 'k--', label='RK4Method h=.2')
    plt.plot(XValuesE, YValuesE, 'r--', label = "Euler h=.2")
    plt.legend()
    plt.xlabel('t')
    plt.ylabel('y')
    plt.title("Eulers Solution V RK4 Solution")
    plt.grid(True)
    plt.show()
    return
    
def Q2b():
    """
    desc: The function that we are estimating
    param: x - the x value
    param: y - the y value
    return: int value after x and y are substituted for the calculation
    """
    def fb(x, y):
        return 4 - x + 2 * y
    
    def exactf(x):
        return -7/4 + 1/2 * x + 11/4 * np.exp(2*x)
    
    #Initialize
    a = 0
    b = 2
    h = .2
    n = int((b-a)/h)
    Yo = 1
    XValuesE = np.linspace(0, 2, n+1)
    XValuesR = np.linspace(0, 2, n+1)
    YValuesE = np.zeros(n+1)
    YValuesR = np.zeros(n+1)
    YValuesE[0] = YValuesR[0] = Yo
    exactXValues = np.linspace(0,2,200)
    exactYValues = exactf(exactXValues)

#Get the Y values at X
    for i in range(10):
        YValuesE[i+1] = EulersMethod(a, b, h, XValuesE[i], YValuesE[i], fb)
        YValuesR[i+1] = RK4Method(h, XValuesR[i], YValuesR[i], fb)
    
    #Plot
    plt.plot(exactXValues, exactYValues, 'g--', label='Exact Solution')
    plt.plot(XValuesR, YValuesR, 'k--', label='RK4Method h=.2')
    plt.plot(XValuesE, YValuesE, 'r--', label = "Euler h=.2")
    plt.legend()
    plt.xlabel('t')
    plt.ylabel('y')
    plt.title("Eulers Solution V RK4 Solution")
    plt.grid(True)
    plt.show()
    return
Q1a()
Q1b()
Q2a()
Q2b()