# input - how to ask the user for information to use in your program
# input("Tell user what data to enter and how to enter it")
# the question to the user is the parameter required for the input function
# store the user input in a variable the data is returned as a string
# strings can be converted by int() or float()

numberEntered = input('Enter any number: ')
# Is the number positive or negative
if int(numberEntered) > 0:
    print('The number is positive')
else:
    print('The number is negative')
# Is the number larger than 100
if int(numberEntered) > 100:
    print('The number is over 100')
# Is the number 5
elif int(numberEntered) == 5:
    print('The number is 5')
else:
    print('The number entered is not larger than 100 and is not 5')

# decision Structures
# if - if, if/else, if/elif/else
# using logic to all your program to make decisions
# > greater than
# < less than
# <= less than or equal to
# >= greater than or equal to
# == equal to
# != not equal to  (not)



# Loops - uses a counter and logic as a termination condition.
# while - uses a counter defined outside of loop, you control when the counter is incremented
# for - used to loop through lists and strings. No counter or condition (foreach loop)
# keywords:
# continue - stops executing code and checks logic to test if loop continues to run.
# pass - skips the rest of the code and continues the program
# break - stops executing code and stops the loop

# create a foreach loop to iterate throught a list of a numbers
listOfNumbers = [2,4,76,3,7,20,15,30]
print(listOfNumbers)
for numbers in listOfNumbers:
    print(numbers)
# print each number and describe them to the console
count = 1
# The first variable int the foreach loop will be the variable assigned for each
# item in the list
# the second variable is the list or dara structure to iterate through
for numbers in listOfNumbers:
    print(f'Number {count}: {numbers})
          count += 1
# functions - a named block of code to perform an action
# call a function
# pass in values to the function called parameters.
# can return a value to the part of the code where called.
# method header comments

# function to find the largest number entered
# the keyword def nameOfFunction:
# two scopes of a method
# global variables scope - a variable usually written at the top of the program and can be used anywhere in your code.
# local variables scope - a variable that can only be used with a block of code.
# () variables inside the initializers is data passed into the method

# function to find the smallest number entered
# if the value entered is smaller than the current smallest value then store it as the largest

# ask the user to enter numbers and enter a q to stop entering numbers
