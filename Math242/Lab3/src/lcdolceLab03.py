"""
MATH 252 Lab 03
Lakota Dolce
Dr. Banjade
"""

#Exercise 1

#Initilize variables
number = 1
i = 0
#Create the loop
for i in range(30):
    #imcrement number by 4
    number += 4
    #increment i by 1
    i+= 1
#Display the number
print (f"The 30th number in the sequence of [1,5,9,13...] is: {number}")

#Exercise 2
#Initialize variables
numbers = []
i = 2
#Create the loop
for i in range(15):
    #Increment number by n^2 + 1
    numbers.append((i+1)**2 + 1)
    #Increment i by 1
    i+= 1
#Print the result
print (f"The first 15 numbers in the sequence of [2,5,10,17...] is: {numbers}")

#Exercise 3
#Initialize Variables
sum = 0
i = 1
for i in range(99):
    #add previous sum to new sum
    sum += i
    #increment i
    i+=2
#Print the results
print (f"The  total of the sum is: {sum}")

#Exercise 4
#Initialize the variables
sum = 0
i = 3
for i in range(33):
    if i <= 33:
        #Add up the previous sum to new sum
        sum += i**3
        #Increment i
        i += 3
    if i == 33:
        i = 40
    if i <=90 and i > 33:
        #Add previous sum to new sum
        sum += i**2
        #increment i
        i +=10
#Print the result
print (f"The  total of the sum is: {sum}")

#Exercise 5
#Initialize variables
sum = 1
i = 0
for i in range(400):
    #Implement number by 
    if i != 0:
        sum += 1 / i
    i += 1
#Print the results
print (f"The  total of the sum is: {sum}")