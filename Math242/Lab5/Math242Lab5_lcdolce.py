"""
Lakota Dolce
Math 242
Lab5
Dr. Debendra
"""
import math

#Exercise 1
def calculateInterest(P, r, n, t):
    balance = P * (1 + r / n) ** (n * t)
    return round(balance,2)

#1a
a = calculateInterest(8000, .04, 12, 10)
print (f"The balance after 10 years compounded monthly with an interest rate of 4% and an initial balance of 8000 is : \n {a}")
#1b
b = calculateInterest(5000, .025, 4, 5)
print (f"The balance after 5 years compounded quarterly with an interest rate of 2.5% and an initial balance of 5000 is : \n {a}")

#Exercise 2
def calculateFib(termWanted):
    #initialize the loop
    i = 0
    term1 = 1
    term2 = 1
    term = 0
    while (i < termWanted - 2):
        if (i % 2 == 0):
            term1+=term2
            term = term1
        else:
            term2 +=term1
            term = term2
        i += 1
    return term

#1a
fib25 = calculateFib(25)
print(f"The 25th term of the fibonacci sequence is {fib25}")

#1b
fib35 = calculateFib(35)
print(f"The 35th term of the fibonacci sequence is {fib35}")

#Exercise 3
def annualLoanPayment (P, n, i):
    A = P * ((i * (1 + i) ** n) / ((1 + i) ** n - 1))
    return round(A,2)

n1 = annualLoanPayment(35000, 1, .076)
n2 = annualLoanPayment(35000, 2, .076)
n3 = annualLoanPayment(35000, 3, .076)
n4 = annualLoanPayment(35000, 4, .076)

print(f"""If n = 1 then the loan payment would be : {n1}
If n = 2 then the loan payment would be : {n2}
If n = 3 then the loan payment would be : {n3}
If n = 4 then the loan payment would be : {n4}
""")

#Exercise 4
def NewtonsMethod(x, f , fprime, i):
    #Calculate the next Xi
    xnext = x - f(x) / fprime(x)
    #Set up a base case to break the recursion
    if (xnext == x or i >= 10):
        return x
    i+= 1
    #Recursively call the function until you get the answer
    return NewtonsMethod(xnext, f, fprime, i)

#4a
print("Using the Newtons Method")
def fa (x):
    return x**3 - 2
def fprimea(x):
    return 3 * x **2

#Get the answers and print
answer = NewtonsMethod(2, fa, fprimea, 0)
print(f"The 10th x would be {round(answer,6)}")

#4b
def fb (x):
    return x**5 - 17
def fprimeb(x):
    return 5 * x**4
#Get the answers and print
answer = NewtonsMethod(2.1, fb, fprimeb, 0)
print(f"The 10th x would be {round(answer,6)}")


#4c
def fc (x):
    return math.sin(x)+ x-1
def fprimec(x):
    return math.cos(x) + 1

#Get the answer and print
answer = NewtonsMethod(1.5, fc, fprimec, 0)
print(f"The 10th x would be {round(answer,6)}")

#4d
def fd (x):
    return math.log(x+1)-1
def fprimed(x):
    return 1/(x+1)

#Get the answer and print
answer = NewtonsMethod(1.7, fd, fprimed, 0)
print(f"The 10th x would be {round(answer,6)}")

#Exercise 5
def calcModifiedSec(x, f, delta, i):
    #Check the base case
    if (i >= 10):
        return x
    xnext = x - f(x) * (delta / (f(x + delta) - f(x)))
    i+= 1
    #recursively call until the answer
    return calcModifiedSec(xnext, f, delta, i)

#5a
print(f"\nThe 10th x using the modified sec method would be {round(calcModifiedSec(2, fa, .001, 0),6)}")
#5b
print(f"The 10th x using the modified sec method would be {round(calcModifiedSec(2.1, fb, .001, 0),6)}")
#5c
print(f"The 10th x using the modified sec method would be {round(calcModifiedSec(1.5, fc, .001, 0),6)}")
#5d
print(f"The 10th x using the modified sec method would be {round(calcModifiedSec(1.7, fd, .001, 0),6)}")