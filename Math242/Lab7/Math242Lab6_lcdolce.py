"""
Lakota Dolce
Math242
Lab 6
Dr. Debendra
"""

#Question 1
"""Write a Python function to calculate the nth Fibonacci number, Fn. Your function should
produce correct outputs for all n including 1 and 2.
"""
print(f"Question 1:-------------------------------------------------\n")
"""
fibonacci
@params -> int n -  an integer value for the nth term in the fib. seq. that the user wants
@returns -> term - the nth term of the fibonacci sequence
@desc -> This function takes in a parameter (n) and solves for the fibonacci sequence at the nth spot
"""
def fibonacci (n):
    #Initialize
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

#Get term number you want
n = input("What term of the fibonnaci sequence would you like to see? ")
#get nth term
term = fibonacci(n)
#print result
print(f"Term {n} in the fibonnacci sequence is {term}")

#Question 2
"""Write a function that takes a number x and returns 5 if x > 1, 10 if x < 1, and 100 if x = 1
"""
print(f"Question 2:-------------------------------------------------\n")

"""
numberComparison
@params -> int x - hold the number to be compared
@returns -> returns an int depending on conditions
@desc -> Compares x to 1 and gives an output based on if it is less than, greater than, or equal to
"""
def numberComparison(x):
    #Compare x
    if x > 1:
        #return the integer
        return 5
    if x < 1:
        return 10
    if x == 1:
        return 100

#Get x
x = input("Pick a random number ")
#Call function
try:
    answer = numberComparison(int(x))
    #Print the result
    print(f"After comparing you got {answer}")
except Exception as e:
    print(e)

#Question 3
"""Recall that the compound interest formula: A = P*(1+r/n)^(n*t)
where P is the principal, r is the interest rate in decimals, t is the time in years, and n is
number of times the interest compounds in a year.
Write a script that asks for the inputs, and calculates the compound interest, A. If the interest
rate is not in between 0 and 1, the code should raise an error message.
(i) P = $8, 000, r = 0.08, n = 12, t = 6
(ii) P = $8, 000, r = 1.08, n = 12, t = 6
"""
print(f"Question 3:-------------------------------------------------\n")
"""
getInterest
@params -> int P - the initial amount
@params -> float r - the rate of interest
@params -> int n - the frequency the interest is compounded per year
@params -> int t - time in years to be compounded
@returns -> float A -  the amount after t years
@desc -> Takes in the principle, rate, frequency and time to calulate the interest from initial conditions
"""
def getInterest(P = 0, n = 0, r = 0, t = 0):
    #Get user input for variables if not already passed
    if P == 0: 
        return ValueError
    #Error check
    if r > 1 or r < 0:
        #return error
        return ValueError
    if r > 0 and r < 1: 
        #calculate amount after t years with rate r and compounded n times
        A = P * (1 + r / t)**(n * t)
        #return answer
        return f"The Amount after interest is {round(A, 2)}"

#3i
#Call the function
principle = input("What is the principle amount? ")
term = input ("What is the term you would like to use? ")
rate = input("What is the rate for the interest? (Must be between 0 and 1) ")
compound = input("How often will it be compounded? ")
try:
    A = getInterest(int(principle), int(compound), float(rate), int(term))
    #print the answer
    print(f"{A}\n")
except Exception as e:
    print(f"The following error occurred, {e}")

#3ii
#Call the function
principle = input("What is the principle amount? ")
term = input ("What is the term you would like to use? ")
rate = input("What is the rate for the interest? (Must be between 0 and 1) ")
compound = input("How often will it be compounded? ")
try:
    A = getInterest(int(principle), int(compound), float(rate), int(term))
    #print the answer
    print(f"{A}\n")
except Exception as a:
    print(f"The following error occurred, {e}")

#Question 4
"""
Write a script that asks for a numeric grade from 0 to 100 and returns a letter grade according
to the following scheme. Your function should raise error if the grade passed in is not
between 0 and 100. Use as few comparisons as possible.
"""
print(f"Question 4:-------------------------------------------------\n")
"""
getGrade
@params -> none
@returns -> int - the grade 
@desc -> takes in a number to check if it is a valid score for a grade
"""
def getGrade():
    #initialize
    grade = 0
    #Get user input for num
    num = input("What is the grade you would like to know? (must be between 0 and 100) ")
    try:
        #Convert to int
        num = int(num)
    
        #error check
        if num > 100 or num < 0:
            raise ValueError

        #compare from high to low
        if num <= 100 and num >= 90:
            #set grade
            grade = "A"
        if num < 90 and num >= 80:
            grade = "B"
        if num < 80 and num >= 70:
            grade = "C"
        if num < 70 and num >= 60:
            grade = "D"
        if num < 60:
            grade = "F"
        #return grade
        return f"The grade is {grade}"
    except Exception as e:
        return "That was not a valid choice \n Error:  {e}\n"
    
print(getGrade())

#Question 5
"""
Create a function for the Newton's method as in Example 7 to approximate the solution
correct up to 10 decimal places using max of 10 iterations.
(a) x^2 -17 = 0, x0 = 40
(b) x^2 -17 = 0, x0 = 200
(c) x^5 -17 = 0, x0 = 5
"""
print(f"Question 5:-------------------------------------------------\n")
"""
NewtonsMethod
@param -> float Xo - The initial value
@param -> function f - the function passed in
@param -> function fprime - the prime of the function
@param -> int i - the incrementer for the function
@return -> float - the answer to newtons method
@desc -> Takes in the initial values needed for the newtons method and applies the formula returning the answer
"""
def NewtonsMethod(Xo, f , fprime, i = 0):
    #Calculate the next Xi
    Xi = Xo - f(Xo) / fprime(Xo)
    #Set up a base case to break the recursion
    if (Xi == Xo or i == 10):
        return Xo
    i+= 1
    #Recursively call the function until you get the answer
    return NewtonsMethod(Xi, f, fprime, i)

#5a
initial = 40
def function1 (x):
    return x**2 - 17
def prime1(x):
    return 2*x

answer = round(NewtonsMethod(initial, function1, prime1),6)
print(f"Newtons method for x^2 - 17 gives us {answer} with an initial value of 40")

#5b
initial = 200
answer = round(NewtonsMethod(initial, function1, prime1),6) 
print(f"Newtons method for x^2 - 17 gives us {answer} with an initial value of 200")

#5c
initial = 5
def function2 (x):
    return x**5 - 17
def prime2 (x):
    return 5*x**4
answer = round(NewtonsMethod(initial, function2, prime2),6)
print(f"Newtons method for x^5 - 17 gives us {answer} with an initial value of 5")