# functions - a named block of code to perform an action
# call a function
# pass in values to the function called parameters.
# can return a value to the part of the code where called.
# method header comments


# the keyword def nameOfFunction:
# two scopes of a method
# global variables scope - a variable usually written at the top of the program and can be used anywhere in your code.
# local variables scope - a variable that can only be used with a block of code.
# () variables inside the initializers is data passed into the method

# function to find the smallest number entered
# if the value entered is smaller than the current smallest value then store it as the largest

# ask the user to enter numbers and enter a q to stop entering numbers

# function to determine if a number is positive or negative
'''Description: This method is designed to determine that the number is positive/ negative
        Parameters:
            number (int): contains the number to check
        Return:
            boolean: true if the value is positive
                     false if the value is negative
'''
def isPositive (number):
    if int(number) > 0:
        return True
    else:
        return False

#test isPositive
result = isPositive(5)
print(f'Is the number positive {result}')
result = isPositive(-5)
print(f'Is the number positive {result}')

# function to find the largest number entered
numbersList = []
count = 1
while count <= 4:
        numbersEntered = input('Enter a number: ')
        numbersList.append(numbersEntered)
        count += 1

'''Description: This method is designed to find the smallest number
        Parameters:
            numbersList (list): contains the numbers to check
        Return:
            lowestNumber (int): the smallest number
'''
def smallestNumber (numbersList):
    lowestNumber = 9999999999999999999
    for number in numberList:
        if number < lowestNumber:
            lowestNumber = number

    return lowestNumber

result = smallestNumber(numbersList)
print(f'The smallest number was {result}')
