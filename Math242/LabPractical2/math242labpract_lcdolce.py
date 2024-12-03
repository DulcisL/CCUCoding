"""
Lakota Dolce
Math 242
Lab Practical 2
Dr. Debendra
"""
import numpy as np
import matplotlib.pyplot as plt
from sympy import *
import math

""" Eulers Method
desc: This is a function to calculate the Eulers method and return a value at time (t)
param: Xo - the initial X value
param: Yo - the initial y value
param: h - the step size of the function
return: value - a value calculated using Eulers method at a time (t)
"""

def EulersMethod(h, X, Y, f):
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

"""
desc - This function is designed to take in the ODE function and find the equation
param - eqn, the original equation passed in
param - initialCond, the initial value passed in
param - newCond, the value you want to find Q at
param - decimal, the number of decimal places to round to
return - mysol, the solution at the new condition
"""

def getODE(eqn, initialCond, newCond, decimal = 2):
    #Set up variables
    Q = Function('Q')
    t = Symbol('t')

    #Get the ODE
    der = Derivative(Q(t), t)
    ode = Eq(der, eqn)

    #Solve at initial condition
    odesol = dsolve(ode, ics={Q(0): initialCond})
    #Seperate the RHS of the eqn
    ans = odesol.rhs

    #solve at new condition
    mysol = ans.subs(t, newCond).evalf()
    return round(mysol, decimal)
    

"""Question 1a
desc: Write a function that is passed a numeric grade from 40 to 100 and returns a letter grade according
to the following scheme. Your function should give an error if the grade passed in is not between 40
and 100. Write your function using as few comparisons as possible
param: int value - The grade value
return string grade - the letter grade
"""
def quest1a(value):
    if value < 40 or value > 100:
        return -1 
    if value >= 85:
        return "A"
    elif value >= 70:
        return "B"
    elif value >= 40:
        return "F"
    return -1

"""Question 1b
desc: (b) Recall that the Fibonacci numbers are defined as follows:
F1 = 1, F2 = 1,
Fi = Fi−1 + Fi−2, i ≥3
Write a function to calculate the nth Fibonacci number, Fn. Your function should produce correct
outputs for all n including 1 and 2, and an error if n is a negative integer.
param: int termWanted - the ith value the user expects
return: int Fi - the number at sequence Fi
"""
def quest1b(termWanted):
    #Initialize
    n = termWanted
    i = 0
    term = 0
    previous = []
    #Set up loop to break when i is greater than n
    try: 
        while i <= int(n):
            #Get first term
            if i == 0:
                #Save to array
                previous.append(0)
                #Set the term
                term = previous[i]
            #Get second and third term
            if i == 1 or i == 2:
                previous.append(1)
                term = previous[i]
            #Get any other term
            if i > 2:
                previous.append(previous[i-1] + previous[i-2])
                term = previous[i]
            #increment i
            i += 1
        #Return term
        return term
    except Exception as e:
        return e

"""Question 2
desc: 2.13 (a) Approximate the solution of the following IVP using RK4 method by creating a function. Round
your answer to six decimal places.

y′ = 2cos(t) −(1/4)y, y(0) = 3, find y(2) using h = 0.1.

(b) Follow Lab 8 to compare by graphs the approximate solutions of the IVPs using Euler’s Method
and RK4 on [1, 4] with the step size h = 0.2 for the following IVP.

y′ = (t^2 −t + 1 −2y)/t, y(1) = 0.5

The exact solution is z(t) = (3t^4 −4^t3 + 6t^2 + 1)/12t^2

param: none
return: none
"""
def quest2():
    #Set up the functions
    def Yp1(t, y):
        return 2*math.cos(t) - (1/4 * t)
    
    def Yp2(t, y):
        return (t**2 - t + 1 - 2*y) / t
    
    def YExact(t):
        return (3*t**4 - 4*t**3 + 6*t**2 + 1) / (12*t**2)
    
    #Initialize variables
    h1 = .1
    h2 = .2
    a = 1
    b1 = 2
    b2 = 4
    Xo = 0
    Yo = 3
    n = int((4-1)/ h2)
    XValues = np.linspace(a, b2, n+1)
    YValues1 = np.zeros(n+1)
    YValues2 = np.zeros(n+1)
    exactXValues = np.linspace(a,b2,200)
    exactYValues = YExact(exactXValues)
    YValues1[0] = YValues2[0] = exactYValues[0] = Yo
    
    #Part A
    print(f"For 2a the result using the RK4 method is {round(RK4Method(h1, Xo, Yo, Yp1),6)}\n")

    #Part B
    #Get the Y values at X
    for i in range(len(XValues)-1):
        YValues1[i+1] = EulersMethod(h2, XValues[i], YValues1[i], Yp2)
        YValues2[i+1] = RK4Method(h2, XValues[i], YValues2[i], Yp2)

    #Plot
    plt.plot(exactXValues, exactYValues, 'k--', label='Exact Solution')
    plt.plot(XValues, YValues1, 'r--', label = "Euler h=.2")
    plt.plot(XValues, YValues2, 'b--', label = "RK4 h=.2")
    plt.legend()
    plt.xlabel('t')
    plt.ylabel('y')
    plt.title("Aproximation Solution vs Exact Solution")
    plt.grid(True)
    plt.show()

""" Question 3
desc: A tank initially contains 400 gal of water with 2% sugar dissolved. A sugar-water solution containing 4
lb of sugar per gal enters the tank at a rate of 3 gal per minute and simultaneously a drain is opened at
the bottom of the tank allowing the well stirred sugar solution to leave at 4 gal per minute. Determine
the sugar content in the tank at the moment when there is 360 gal of mixture left
(i) use Euler’s Method with h = 0.1
(ii) use RK4 method with h = 0.2
(ii) Find the exact value using numpy.
param: none
return: none
"""
def quest3():
    """
    dV/dt = 3 - 4 = -1
    equation: dQ/dt = 3*4 - 4*q/(400-t)
    f(0) = 400 * .2
    t = 400-360 = 40
    f(40) = ?
    """
    #Set up the function
    def f(X, Y):
        return 12 - ((4 * Y) / (400 - X))
    
    #Initialize
    a = 0
    b = 40
    hE = .1
    hR = .2
    QE = QR = initialCond = 400 *.2
    newCond = 40
    
    #Estimate
    #Set up loop
    t = a
    while t < b:
        QE = EulersMethod(hE, t, QE, f)
        t += hE
    
    #Reset for RK4 Method
    t = a
    while t < b:
        QR = RK4Method(hR, t, QR, f)
        t += hR

    #Eulers Method
    print(f"The Eulers estimation for the IVP Tank problem is {round(QE, 2)}")

    #RK4 Method
    print(f"The RK4 estimation for the IVP Tank problem is {round(QR, 2)}")


    #Exact
    #Set up equation
    Q = Function('Q')
    t = Symbol('t')
    eqn = 12 - ((4 * Q(t)) / (400 - t))

    #Get the solution
    print(f"{getODE(eqn, initialCond, newCond)} lbs of sugar")
    return

#Call functions and get answers
print("\n-----------------------------------------------\n")
#Error check values for valid input
while True:
    try:
        value = int(input("What grade do you want to know the letter value for? \n"))
        grade = quest1a(value)
        #If function returns a -1 it's not a valid input
        if grade == -1:
            print("Not a valid grade\n")
            continue
        #If all is good print the grade
        else:
            print(f"The letter grade is a(n) {grade}\n")
            break
    except Exception as e:
        print(e)
        continue

#Error check i for valid input
while True:
    try:
        i = int(input("What term of the fibonacci sequence do you want? \n"))
        #Check if the number is above zero
        if i <=0:
            print("Not a valid number\n")
            continue
        #Otherwise run the function for the number at Fi
        else:
            print(f"The number at F{i} is {round(quest1b(i),6)}\n")
            break
    except Exception as e:
        print(e)
        continue

quest2()
quest3()
