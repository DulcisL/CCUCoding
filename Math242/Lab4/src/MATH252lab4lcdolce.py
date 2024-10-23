"""Lakota Dolce
Math 252
Lab 4
Dr. Debendra
"""
import math

#Exercise 1 Exponentions smoothing A = .2
#Initialize
points = [32, 46, 39, 50, 41, 60, 50, 47, 51, 42, 33, 28, 45, 55, 42, 67]
result = 0
alpha = .2
previous = []
#Set up the loop
for i in range(len(points)):
    #check for the first run in the loop
    if i > 0 :
        #Calculate and set the array values
        previous.append(round((alpha * points[i]) + (1-alpha) * (previous[i - 1]), 2))
    if i == 0:
        #initial condition for the first run
        previous.append(points[i])

#Print the answer
print(f"The smoothed points are {previous}")

#Exercise 2 Calculate the fibonacci's 25th number
#Initialize
fib = [1,1]

#set up loop
for i in range(25):
    #Check for the first 2 runs
    if i < 1:
        continue
    if i > 1:
        #take the previous numbers and add them to get the next
        fib.append(fib[i-1] +  fib[i-2])

#Arrays start at 0
print(f"{fib[24]} is the 25th number in the fibonacci sequence")

#Exercise 3 Print the first 15 of the the lucas numbers
#Initialize
lnumbers = [2,1]
#Set up the loop
for i in range(15):
    #Check for initial conditions
    if i < 1:
        continue
    if i > 1:
        #Compute the next in line by taking the previous two in the array
        lnumbers.append(lnumbers[i-1] + lnumbers[i-2])
    
#print the result
print(f"The first 15 numbers of the lucas numbers are {lnumbers}")

#Exercise 4 Calculate the depreciation of the initial investment after 8 years at 7.5%/yr
#Initialize variables
initial = 5000

#Set up the loop
for i in range(8):
    #Calculate the interest for the year
    initial = initial * .925
    #Print the result
print(f"The Initial investment would have a value of ${round(initial,2)}")

#Exercise 5 Calculate the growth of a fish at 20 days
#Initialize
size = 5
#Set up the loop for the first growth rate
for i in range(10):
    #Calculate the size difference
    size = size * 1.2

#Change the growth rate
for i in range(10):
    #Calculate the new size
    size = size * 1.15

#Print the result
print(f"The size after 20 days would be {round(size, 2)}mm")

#Exercise 6 Use Newtons method to calc X0 to X10
#Set up the base function for the Newton method
def NewtonsMethod(x, f , fprime):
    #Set up a base case to break the recursion
    if x > 10:
        return x
    if x <= 10:
        #Calculate the next Xi
        xnext = x - f(x) / fprime(x)
        #Recursively call the function until you get the answer
        return xnext, f, fprime
    
#(a) x^3-2 = 0 , x0 = 2

#Set up the equations
def fa (x):
    return x**3 - 2
def fprimea(x):
    return 3 * x **2

#Get the answers and print
answer, blah, blah2 = NewtonsMethod(2, fa, fprimea)
print(f"The 10th x would be {round(answer,6)}")

#(b) x^5-17 = 0, x0 = 2.1

#Set up the equations
def fb (x):
    return x**5 - 17
def fprimeb(x):
    return 5 * x**4

#Get the answers and print
answer, blah, blah2 = NewtonsMethod(2.1, fb, fprimeb)
print(f"The 10th x would be {round(answer,6)}")

#(c) sin(x)+x-1 = 0 , x0 = 1.5

#Set up the equations
def fc (x):
    return math.sin(x)+ x-1
def fprimec(x):
    return math.cos(x) + 1

#Get the answer and print
answer, blah, blah2 = NewtonsMethod(1.5, fc, fprimec)
print(f"The 10th x would be {round(answer,6)}")

#(d) ln(x+1) = 1 , x0 = 1.7
#Set up the equations
def fd (x):
    return math.log(x+1)-1
def fprimed(x):
    return 1/(x+1)

#Get the answer and print
answer, blah, blah2 = NewtonsMethod(1.7, fd, fprimed)
print(f"The 10th x would be {round(answer,6)}")