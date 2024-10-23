"""
Lakota Dolce
Lab Practical
10/14/2024
Dr. Debendra
"""
#Needed libraries
import numpy as np
import matplotlib.pyplot as plt
import math

#Question 1a
#Title and label variables
title = "Lab Practical 1 2D graph"
horizontal=""
vertical = ""
gridTF = True
fsize = 20 #Font size
lwidth = 1; #line width
lstyle = "solid" #line style
lcolor = "" #line color
llabel = "" 
start = 3
stop = 8
accuracy = 300

#Function
t = np.linspace(start,stop, accuracy) #(start, stop, # of points)
ft = ((7 * t**2 / 80) - (np.sqrt((t + 4)) / 2))

#Plotting
plt.plot(t,ft, linestyle = lstyle, linewidth = lwidth, label = llabel)
plt.title(title,fontsize = fsize)   
plt.xlabel(horizontal)
plt.ylabel(vertical)
plt.legend() 
plt.grid(gridTF)
plt.show()

#Question 1b
#Title and label variables
title = "Lab Practical 1 2D graph"
horizontal=""
vertical = ""
gridTF = True
fsize = 20 #Font size
lwidth = 1; #line width
lstyle = "solid" #line style
lcolor = "" #line color
llabel = "" 
start = 0
stop = 8
accuracy = 300
gap = 1

#Function
t = np.linspace(start,stop, accuracy) #(start, stop, # of points)
ft = (1/2 * np.exp(.2*t)*np.sin(t))
t2 = np.arange(start,stop, gap)
y = [0.2, 1, 0.5, -0.25, -0.3, -1, 0.2, 1]

#Plotting
plt.plot(t,ft, linestyle = lstyle, linewidth = lwidth, label = llabel)
plt.plot(t2, y, "*")
plt.title(title,fontsize = fsize)   
plt.xlabel(horizontal)
plt.ylabel(vertical)
plt.legend() 
plt.grid(gridTF)
plt.show()

#Question 2a
#Initialize
j = 10
sum = 0
#loop
for i in range(50):
    #Calculate n^2 terms
    if i >= 3 and i <= 21:
        sum += 1/(i**2)
        i +=2
        #Calculate the n^3 terms
    if i > 21:
        sum += 1/ (j**3)
        j += 10
        #Increment I by 2.9 to prevent excess runs
        i += 2.9
#Print the sum
print(f"The sum is {round(sum,6)}")

#Question 2b
#Initialize
count = 0
a = 2
#Set up a loop to run 12 times
while count < 12:
    #Get the new term
    term = 2* a + 1
    #print out the term 
    print(f"term {count +1} is {round(a,6)}")
    #Save it for next run
    a = term
    #increment count
    count += 1

#Question 3b
#set up the function
def NewtonsMethod(x, f , fprime):
    #Calculate the next Xi
    xnext = x - f(x) / fprime(x)
    #Set up a base case to break the recursion
    if (xnext == x):
        return x
    #Return the next term
    return xnext

#Set up the functions themselves
def fa (x):
    return x**2 - math.exp(x) + 2
def fprimea(x):
    return 2 * x - math.exp(x)

#Inititialize
term = 2
i = 0
#Set up the loop
while i <= 10:
    #Print the current term
    print(f"Term {i} of the newtons method is {round(term,8)}")
    #Get the next term
    term = NewtonsMethod(term, fa, fprimea)
    #increment the counter
    i+=1

#Question 4a
#Set up the function
def FindRoots(a,b,c):
    #Make sure roots can be calculated
    if (b**2 - 4 * a * c) > 0:
        #Calculate roots
        r1 = (-b + math.sqrt(b**2 - 4 * a * c)) / (2 * a)
        r2 = (-b - math.sqrt(b**2 - 4 * a * c)) / (2 * a)
        #return roots
        return round(r1,6), round(r2,6)
    #Otherwise return no roots
    else:
        return "There are no roots", ""

#Get the roots
root1, root2 = FindRoots(2, -1, -6)
#Print the answer
print(f"The roots of 2x^2-x-6: {root1}, {root2}")
#Get the roots
root1, root2 = FindRoots(3, 2, -8)
#Print the answer
print(f"The roots of 3x^2+2x-8: {root1}, {root2}")

#Question 4b
#Initialize
smoothed = []
alpha = .25
points = [50,45,32,56,83,58,34,48,33,66,49]
#Get smoothed points using loop
for i in range(len(points)):
    #add them to the new array
    #Check if it is the first run or not
    if i >= 1:
        point = points[i]
        previous = smoothed[i-1]
        smoothed.append(round(((alpha * point) + (1 - alpha) * previous),2))
    else:
        smoothed.append(points[i])
#print the new array
print("The smoothed data points")
for i in range(len(smoothed)):
    print(f"Point {i + 1} is {round(smoothed[i],6)}")

#Question 5a
#Calculate the volume
def calculateVolume(r, h):
    return round(((1/3) * math.pi * (r**2) * h), 6)
#Calculate the surface area
def calculateSurfaceArea (r, h):
    return round(math.pi * r * (r + math.sqrt((h**2) + (r**2))),6)

#Print the answers
print(f"The Volume is {calculateVolume(2, 10)}, The surface area is {calculateSurfaceArea(2, 10)}")

#Question 5b
#Initialize
array = []
#Set up the loop to run 18 times
for n in range(18):
    #add to array
    array.append(2 * (n**2) - 1)
#Print out the anser (array starts at 0)
print(f"The 18th term is {round(array[17],6)}")