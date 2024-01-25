#program header
''' Name: Lakota Dolce
Date: 2/1/2023
Assignment: Wk 04 Assignment 2
Pseudocode:

INPUT:

User tells the console how many numbers they want to add to the list

PROCESSING:

Check the input for proper choice
        TRUE: convert to integer and continue program
        FALSE: Ask the user for a corrected input
Ask the user for the numbers they wanted to add
    INPUT: Enter number here:
    STORE as newNumber
    Check for proper input
        TRUE: APPEND to numbers list
        FALSE: Ask user for an actual number
    Continue until number of numbers = user choice
Find the smallest number in the list
    Iterate through the list
        set up for loop and compare each number for smallest
    RETURN the smallest number
Find the sum of the list
    Iterate through the list and add each number
        save the first number as the total and continue
    RETURN the total number
Find the average of the list
    take the sum and divide by the length of the list
    RETURN the average

OUTPUT:

PRINT the smallest, average, and sums to the console with descriptions
'''

'''Description: This method is designed to sum the numbers in the list
        Parameters:
            numbers (list): contains the list of numbers from the user
        Return:
            total (int): The total of that sum
'''
def sums (numbers):
    x = 0
    # iterate through the list
    for x in range(len(numbers)):
        # add the numbers together
        try:
            total = numbers[0]
            numbers[0] += numbers[x+1]
        except IndexError:
            continue
        except UnboundLocalError:
            print('There are no numbers')
        finally:
            continue
    return total

'''Description: This method is designed to find the smallest number in a list
        Parameters:
            numbers (list): contains the list of numbers from the user
        Return:
            smallest (int): smallest number
'''
def smallestNumber(numbers):
    # Iterate through the list
    try:
        smallest = numbers[0]
        x = 0
        while x < len(numbers):
            #compare the list for smallest number
            if smallest >= numbers[x]:
                smallest = numbers[x]
            x += 1
    except IndexError:
        print('There are no numbers')
        smallest = 'none'
    finally:
        return smallest

'''Description: This method is designed to average out the numbers in the list
        Parameters:
            numbers (list): contains the list of numbers from the user
            sum (int): contains the sum of the list previously calculated
        Return:
            average (flt): The average of the numbers
'''
def averageNumber(numbers, sum):
    try:
        average = sum / len(numbers)
    except ZeroDivisionError:
        print('There is no average')
        average = 0
    finally:
        return average

# Ask for how many numbers the user wants
incorrect = True
desires = input('How many numbers do you want to add (enter an integer)? ')
while incorrect == True:
    try:
        desires = int(desires)
        incorrect = False
        if desires < 0:
            raise ValueError
    except ValueError:
        print('Not a valid number try again')
        desires = input('How many numbers do you want to add (enter an integer)? ')
    except TypeError:
        print('Not a valid number try again')
        desires = input('How many numbers do you want to add (enter an integer)? ')
# Create loop to add numbers to a list
numbers = []
runs = 0
while runs < desires:
    runs += 1
    newNumber = input(f'Enter number {runs} here: ')
    incorrect = True
    while incorrect == True:
        try:
            newNumber = int(newNumber)
            numbers.append(newNumber)
            incorrect = False
            continue
        except ValueError:
            print('You did not enter a number, please try again \n')
            newNumber = input(f'Please enter number {runs}: ')
        finally:
            print('Thank you \n')


# Print all statements
smallest = smallestNumber(numbers)
sum = sums(numbers)
averages = averageNumber(numbers, sum)
print(f'You wanted {desires} numbers')
print(f'The sum of the numbers was {sum}')
print(f'The smallest number was {smallest}')
print(f'The average was {averages}')