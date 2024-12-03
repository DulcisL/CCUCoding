"""
Lakota Dolce
Math242
Lab 9
Dr. Debendra
"""

from sympy import *

"""
Desc - This function is designed to take in the ODE function and find the equation
Param - eqn, the original equation passed in
Param - initialCond, the initial value passed in
Param - newCond, the value you want to find Q at
Param - decimal, the number of decimal places to round to
Return - mysol, the solution at the new condition
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

"""
Desc - This function is designed to solve the problem at Q1 of the lab
Question 1: A tank initially contains 500 gal of water with 2% sugar dissolved. A sugar-water solution containing 2 lb of
sugar per gal enters the tank at a rate of 3 gal per minute and simultaneously a drain is opened at the bottom of
the tank allowing the well stirred sugar solution to leave at 4 gal per minute. Determine the sugar content in the
tank at the moment when there is 350 gal of mixture left.
Hint: Find the V, which is V(t) = -t + 500. Find t when V is 350. Then find Q at that time like in example 2

"""

def Q1():
    #Initialize variables
    #dV/dt = 3gal/min - 4gal/min = -1t
    #dQ/dt = 3*2 - (4*Q)/(500-t) = 6 - (4*Q)/(500-t)

    #At t=0 Q(0) = 500gal at 2% solution
    initialCond = 500 * .02
    #solve for t (500-t = 350gal) = 150
    newCond = 150 
    #Set up equation
    Q = Function('Q')
    t = Symbol('t')
    eqn = 6 - (4 * Q(t)) / (500-t)

    #Get the solution
    print(f"{getODE(eqn, initialCond, newCond)} lbs of sugar")
    return


"""
Desc - This function is designed to solve the problem at Q2 of the lab
Question 2: A tank with a capacity of 500 gal originally contains 200 gal of water with 100 lb of salt in solution. Water
containing 1 lb of salt per gallon is entering at a rate of 3 gal/min, and the mixture is allowed to flow out of the
tank at a rate of 2 gal/min. Find the amount of salt in the tank at the moment when the solution begins to overflow.
Hint: Find Q at the time when V is 500. Find V and set it to 500 to get the time
"""
def Q2():
    #Initialize variables
    #dV/dt = 3gal/min - 2gal/min = t
    #dQ/dt = 3*1 - (2*Q)/(200+t) = 3 - (2*Q)/(200+t)

    #At t=0 Q(0) = 200gal @ 100lbs
    initialCond = 100
    #solve for t (200 + t = 500gal) = 300
    newCond = 300 
    #Set up equation
    Q = Function('Q')
    t = Symbol('t')
    eqn = 3 - ((2 * Q(t)) / (200 + t))

    #Get the solution
    print(f"{getODE(eqn, initialCond, newCond)} lbs of salt")
    return

Q1()
Q2()